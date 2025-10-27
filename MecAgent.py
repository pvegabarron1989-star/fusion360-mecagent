"""
MecAgent - Asistente IA para Fusion 360
Integración con Claude API para construcción asistida de proyectos CAD
"""

import adsk.core, adsk.fusion, adsk.cam, traceback
import os
import sys
import json

# Agregar el path de librerías
lib_path = os.path.join(os.path.dirname(__file__), 'lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

from claude_integration import ClaudeAssistant
from cad_executor import CADExecutor

# Variables globales
_app = adsk.core.Application.cast(None)
_ui = adsk.core.UserInterface.cast(None)
_handlers = []
_palette = None

# Configuración
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

def run(context):
    """Punto de entrada del add-in"""
    global _app, _ui
    try:
        _app = adsk.core.Application.get()
        _ui = _app.userInterface
        
        # Cargar configuración
        if not os.path.exists(CONFIG_FILE):
            _ui.messageBox(
                '⚠️ No se encontró config.json\n\n'
                'Por favor copia config_template.json a config.json '
                'y agrega tu API key de Claude.',
                'MecAgent - Configuración Requerida'
            )
            return
        
        # Crear el botón del panel
        crear_panel_ui()
        
        _ui.messageBox(
            '✅ MecAgent iniciado correctamente!\n\n'
            'Haz clic en el botón "MecAgent Chat" para comenzar.',
            'MecAgent'
        )
        
    except:
        if _ui:
            _ui.messageBox('Error al iniciar MecAgent:\n{}'.format(traceback.format_exc()))


def stop(context):
    """Limpieza al detener el add-in"""
    global _ui, _palette
    try:
        if _palette:
            _palette.deleteMe()
        
        # Eliminar elementos del UI
        eliminar_panel_ui()
        
    except:
        if _ui:
            _ui.messageBox('Error al detener:\n{}'.format(traceback.format_exc()))


def crear_panel_ui():
    """Crea el botón en el panel de Fusion 360"""
    global _ui
    
    # Obtener el panel de herramientas
    toolbarPanel = _ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
    if not toolbarPanel:
        toolbarPanel = _ui.allToolbarPanels.item(0)
    
    # Crear el botón
    buttonDef = _ui.commandDefinitions.itemById('MecAgentChatButton')
    if not buttonDef:
        buttonDef = _ui.commandDefinitions.addButtonDefinition(
            'MecAgentChatButton',
            'MecAgent Chat',
            'Asistente IA con Claude para construcción de proyectos CAD',
            './resources'
        )
    
    # Crear el evento del botón
    onCommandCreated = MecAgentCommandCreatedHandler()
    buttonDef.commandCreated.add(onCommandCreated)
    _handlers.append(onCommandCreated)
    
    # Agregar el botón al panel
    buttonControl = toolbarPanel.controls.itemById('MecAgentChatButton')
    if not buttonControl:
        buttonControl = toolbarPanel.controls.addCommand(buttonDef)
        buttonControl.isPromoted = True


def eliminar_panel_ui():
    """Elimina los elementos del UI"""
    global _ui
    
    toolbarPanel = _ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
    if toolbarPanel:
        buttonControl = toolbarPanel.controls.itemById('MecAgentChatButton')
        if buttonControl:
            buttonControl.deleteMe()
    
    buttonDef = _ui.commandDefinitions.itemById('MecAgentChatButton')
    if buttonDef:
        buttonDef.deleteMe()


class MecAgentCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    """Manejador de eventos para el comando del botón"""
    
    def __init__(self):
        super().__init__()
    
    def notify(self, args):
        try:
            command = args.command
            onExecute = MecAgentCommandExecuteHandler()
            command.execute.add(onExecute)
            _handlers.append(onExecute)
        except:
            _ui.messageBox('Error en CommandCreated:\n{}'.format(traceback.format_exc()))


class MecAgentCommandExecuteHandler(adsk.core.CommandEventHandler):
    """Manejador de ejecución del comando"""
    
    def __init__(self):
        super().__init__()
    
    def notify(self, args):
        try:
            abrir_palette_chat()
        except:
            _ui.messageBox('Error al abrir chat:\n{}'.format(traceback.format_exc()))


def abrir_palette_chat():
    """Abre el panel de chat de MecAgent"""
    global _palette, _ui
    
    # Si ya existe, mostrarlo
    if _palette:
        _palette.isVisible = True
        return
    
    # Crear nuevo palette
    html_file = os.path.join(os.path.dirname(__file__), 'chat_ui.html')
    _palette = _ui.palettes.add(
        'MecAgentChatPalette',
        'MecAgent - Asistente IA',
        html_file,
        True,  # isVisible
        True,  # showCloseButton
        True,  # isResizable
        400,   # width
        600    # height
    )
    
    # Eventos del palette
    onHTMLEvent = MecAgentHTMLEventHandler()
    _palette.incomingFromHTML.add(onHTMLEvent)
    _handlers.append(onHTMLEvent)
    
    onClosed = MecAgentPaletteClosedHandler()
    _palette.closed.add(onClosed)
    _handlers.append(onClosed)


class MecAgentHTMLEventHandler(adsk.core.HTMLEventHandler):
    """Manejador de mensajes desde el HTML"""
    
    def __init__(self):
        super().__init__()
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        self.claude = ClaudeAssistant(config['claude_api_key'])
        self.executor = CADExecutor(_app)
    
    def notify(self, args):
        try:
            mensaje = args.data
            data = json.loads(mensaje)
            
            if data['action'] == 'send_message':
                user_message = data['message']
                
                # Obtener respuesta de Claude
                respuesta = self.claude.procesar_mensaje(user_message)
                
                # Ejecutar comandos CAD si los hay
                if respuesta.get('commands'):
                    resultado = self.executor.ejecutar_comandos(respuesta['commands'])
                    respuesta['execution_result'] = resultado
                
                # Enviar respuesta al HTML
                _palette.sendInfoToHTML('response', json.dumps(respuesta))
                
        except:
            error_msg = traceback.format_exc()
            _palette.sendInfoToHTML('error', error_msg)


class MecAgentPaletteClosedHandler(adsk.core.UserInterfaceGeneralEventHandler):
    """Manejador de cierre del palette"""
    
    def __init__(self):
        super().__init__()
    
    def notify(self, args):
        global _palette
        _palette = None
