# 🤖 MecAgent - Asistente IA para Fusion 360

MecAgent es un add-in para Autodesk Fusion 360 que integra Claude API de Anthropic para proporcionar un asistente de IA conversacional que ayuda a construir proyectos CAD mediante lenguaje natural.

![MecAgent Banner](https://img.shields.io/badge/Fusion%20360-Add--in-blue?style=for-the-badge&logo=autodesk)
![Claude API](https://img.shields.io/badge/Claude-3.5%20Sonnet-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.7+-green?style=for-the-badge&logo=python)

## ✨ Características

- 💬 **Chat en tiempo real** integrado en Fusion 360
- 🧠 **Procesamiento de lenguaje natural** con Claude 3.5 Sonnet
- 🛠️ **Ejecución automática de comandos CAD**
- 🎨 **Interfaz moderna y amigable**
- 🌐 **Soporte completo en español**
- 📚 **Historial de conversación**

## 🚀 Instalación

### Requisitos previos

1. **Autodesk Fusion 360** instalado
2. **Python 3.7+** (viene incluido con Fusion 360)
3. **API Key de Claude** ([obtener aquí](https://console.anthropic.com/))

### Pasos de instalación

1. **Clona este repositorio:**
   ```bash
   git clone https://github.com/pvegabarron1989-star/fusion360-mecagent.git
   ```

2. **Localiza la carpeta de Add-ins de Fusion 360:**
   - **Windows**: `C:\Users\<TuUsuario>\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\`
   - **Mac**: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/`

3. **Copia la carpeta del proyecto** a la carpeta de Add-ins

4. **Instala las dependencias:**
   ```bash
   cd fusion360-mecagent
   pip install -r requirements.txt
   ```

5. **Configura tu API Key:**
   - Copia `config_template.json` a `config.json`
   - Edita `config.json` y agrega tu Claude API key:
   ```json
   {
     "claude_api_key": "sk-ant-api03-XXXXXXX"
   }
   ```

6. **Inicia Fusion 360** y ve a:
   - **Tools** > **Add-Ins** > **Scripts and Add-Ins**
   - En la pestaña **Add-Ins**, busca **MecAgent**
   - Haz clic en **Run**

## 💡 Uso

### Comandos de ejemplo

Una vez iniciado MecAgent, verás un botón "MecAgent Chat" en el panel de herramientas. Haz clic para abrir el chat y prueba estos comandos:

```
"Crea un círculo de 50mm de diámetro"
"Dibuja un rectángulo de 30mm x 40mm"
"Extruye el perfil 25mm"
"Ayúdame a diseñar un engranaje"
"Crea un cilindro de 20mm de diámetro y 50mm de altura"
```

### Comandos CAD disponibles

| Comando | Descripción | Parámetros |
|---------|-------------|------------|
| `sketch_circle` | Dibuja un círculo | diameter, center |
| `sketch_rectangle` | Dibuja un rectángulo | width, height, center |
| `sketch_line` | Dibuja una línea | start, end |
| `extrude` | Extruye un perfil | distance |
| `revolve` | Crea una revolución | angle |
| `fillet` | Redondea aristas | radius |
| `chamfer` | Crea chaflanes | distance |

## 📁 Estructura del proyecto

```
fusion360-mecagent/
├── MecAgent.py              # Add-in principal
├── claude_integration.py    # Integración con Claude API
├── cad_executor.py         # Ejecutor de comandos CAD
├── chat_ui.html            # Interfaz de usuario del chat
├── config_template.json    # Plantilla de configuración
├── config.json            # Configuración (no incluir en git)
├── requirements.txt       # Dependencias de Python
├── README.md             # Este archivo
└── docs/
    └── INSTALLATION_ES.md  # Guía detallada de instalación
```

## 🔧 Desarrollo

### Agregar nuevos comandos CAD

1. Edita `cad_executor.py`
2. Agrega un nuevo método para tu comando:
   ```python
   def mi_nuevo_comando(self, params):
       # Tu implementación aquí
       pass
   ```
3. Actualiza el `system_prompt` en `claude_integration.py`

### Testing

Para probar cambios:
1. Guarda tus archivos
2. En Fusion 360: **Tools** > **Add-Ins** > **Scripts and Add-Ins**
3. Detén el add-in y vuelve a ejecutarlo

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si quieres mejorar MecAgent:

1. Fork este repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Roadmap

- [ ] Soporte para más comandos CAD
- [ ] Reconocimiento de voz
- [ ] Exportar conversaciones
- [ ] Plantillas de diseño predefinidas
- [ ] Integración con GitHub para versionado de diseños
- [ ] Modo de aprendizaje para comandos personalizados

## ⚠️ Troubleshooting

### Error: "No se encontró config.json"
- Asegúrate de copiar `config_template.json` a `config.json`
- Verifica que el archivo esté en la raíz del proyecto

### Error: "Failed to connect to Claude API"
- Verifica tu API key en `config.json`
- Comprueba tu conexión a internet
- Revisa tu cuota de uso en Anthropic Console

### El botón no aparece en Fusion 360
- Reinicia Fusion 360
- Verifica que el add-in esté en la carpeta correcta
- Revisa los logs en: **Tools** > **Add-Ins** > **Scripts and Add-Ins** > **MecAgent** > **Debug**

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👤 Autor

**Pablo Vega Barrón**
- GitHub: [@pvegabarron1989-star](https://github.com/pvegabarron1989-star)

## 🙏 Agradecimientos

- [Anthropic](https://www.anthropic.com/) por Claude API
- [Autodesk](https://www.autodesk.com/) por Fusion 360
- La comunidad de desarrolladores de Fusion 360

---

**¿Te gusta MecAgent? ¡Dale una ⭐ al repositorio!**
