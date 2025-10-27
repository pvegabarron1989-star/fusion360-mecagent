"""
Módulo de integración con Claude API
"""

import anthropic
import json

class ClaudeAssistant:
    """Asistente basado en Claude API"""
    
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.conversation_history = []
        
        # Sistema de prompts para CAD
        self.system_prompt = """Eres MecAgent, un asistente experto en diseño CAD integrado en Fusion 360.

Tu trabajo es ayudar a los usuarios a crear diseños mecánicos mediante comandos de Fusion 360.

Cuando el usuario te pida crear geometría, debes responder en formato JSON con:
{
    "message": "Respuesta amigable al usuario en español",
    "commands": [
        {"type": "sketch_circle", "params": {"diameter": 50, "center": [0, 0]}},
        {"type": "extrude", "params": {"distance": 30}}
    ]
}

Comandos disponibles:
- sketch_circle: Dibuja un círculo (params: diameter, center)
- sketch_rectangle: Dibuja un rectángulo (params: width, height, center)
- sketch_line: Dibuja una línea (params: start, end)
- extrude: Extruye un perfil (params: distance)
- revolve: Revolución (params: angle)
- fillet: Redondeo (params: radius)
- chamfer: Chaflán (params: distance)

Siempre sé útil, claro y amigable. Explica lo que estás haciendo en español."""
    
    def procesar_mensaje(self, mensaje_usuario):
        """Procesa un mensaje del usuario y obtiene respuesta de Claude"""
        
        # Agregar mensaje del usuario al historial
        self.conversation_history.append({
            "role": "user",
            "content": mensaje_usuario
        })
        
        try:
            # Llamar a Claude API
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                system=self.system_prompt,
                messages=self.conversation_history
            )
            
            # Extraer respuesta
            respuesta_texto = response.content[0].text
            
            # Agregar respuesta al historial
            self.conversation_history.append({
                "role": "assistant",
                "content": respuesta_texto
            })
            
            # Intentar parsear como JSON
            try:
                respuesta_json = json.loads(respuesta_texto)
                return respuesta_json
            except:
                # Si no es JSON, devolver como mensaje simple
                return {
                    "message": respuesta_texto,
                    "commands": []
                }
                
        except Exception as e:
            return {
                "message": f"❌ Error al comunicarse con Claude: {str(e)}",
                "commands": []
            }
    
    def limpiar_historial(self):
        """Limpia el historial de conversación"""
        self.conversation_history = []
