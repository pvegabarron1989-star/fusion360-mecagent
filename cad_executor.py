"""
Ejecutor de comandos CAD en Fusion 360
"""

import adsk.core, adsk.fusion
import traceback

class CADExecutor:
    """Ejecuta comandos CAD basados en instrucciones de la IA"""
    
    def __init__(self, app):
        self.app = app
        self.ui = app.userInterface
        self.design = adsk.fusion.Design.cast(app.activeProduct)
        self.rootComp = self.design.rootComponent
    
    def ejecutar_comandos(self, commands):
        """Ejecuta una lista de comandos CAD"""
        resultados = []
        
        for cmd in commands:
            try:
                cmd_type = cmd.get('type')
                params = cmd.get('params', {})
                
                if cmd_type == 'sketch_circle':
                    resultado = self.crear_circulo(params)
                elif cmd_type == 'sketch_rectangle':
                    resultado = self.crear_rectangulo(params)
                elif cmd_type == 'sketch_line':
                    resultado = self.crear_linea(params)
                elif cmd_type == 'extrude':
                    resultado = self.extruir(params)
                elif cmd_type == 'revolve':
                    resultado = self.revolucion(params)
                elif cmd_type == 'fillet':
                    resultado = self.redondeo(params)
                elif cmd_type == 'chamfer':
                    resultado = self.chaflan(params)
                else:
                    resultado = f"⚠️ Comando desconocido: {cmd_type}"
                
                resultados.append(resultado)
                
            except Exception as e:
                resultados.append(f"❌ Error en {cmd_type}: {str(e)}")
        
        return resultados
    
    def crear_circulo(self, params):
        """Crea un círculo en un sketch"""
        try:
            # Crear sketch en plano XY
            sketches = self.rootComp.sketches
            xyPlane = self.rootComp.xYConstructionPlane
            sketch = sketches.add(xyPlane)
            
            # Obtener parámetros
            diameter = params.get('diameter', 10) / 10  # Convertir mm a cm
            center_x = params.get('center', [0, 0])[0] / 10
            center_y = params.get('center', [0, 0])[1] / 10
            
            # Dibujar círculo
            circles = sketch.sketchCurves.sketchCircles
            centerPoint = adsk.core.Point3D.create(center_x, center_y, 0)
            circle = circles.addByCenterRadius(centerPoint, diameter / 2)
            
            return f"✅ Círculo creado: diámetro {params.get('diameter', 10)}mm"
            
        except Exception as e:
            return f"❌ Error al crear círculo: {str(e)}"
    
    def crear_rectangulo(self, params):
        """Crea un rectángulo en un sketch"""
        try:
            sketches = self.rootComp.sketches
            xyPlane = self.rootComp.xYConstructionPlane
            sketch = sketches.add(xyPlane)
            
            width = params.get('width', 10) / 10
            height = params.get('height', 10) / 10
            center = params.get('center', [0, 0])
            cx, cy = center[0] / 10, center[1] / 10
            
            # Calcular esquinas
            p1 = adsk.core.Point3D.create(cx - width/2, cy - height/2, 0)
            p2 = adsk.core.Point3D.create(cx + width/2, cy + height/2, 0)
            
            # Dibujar rectángulo
            lines = sketch.sketchCurves.sketchLines
            lines.addTwoPointRectangle(p1, p2)
            
            return f"✅ Rectángulo creado: {params.get('width')}x{params.get('height')}mm"
            
        except Exception as e:
            return f"❌ Error al crear rectángulo: {str(e)}"
    
    def crear_linea(self, params):
        """Crea una línea en un sketch"""
        try:
            sketches = self.rootComp.sketches
            xyPlane = self.rootComp.xYConstructionPlane
            sketch = sketches.add(xyPlane)
            
            start = params.get('start', [0, 0])
            end = params.get('end', [10, 10])
            
            p1 = adsk.core.Point3D.create(start[0]/10, start[1]/10, 0)
            p2 = adsk.core.Point3D.create(end[0]/10, end[1]/10, 0)
            
            lines = sketch.sketchCurves.sketchLines
            lines.addByTwoPoints(p1, p2)
            
            return f"✅ Línea creada"
            
        except Exception as e:
            return f"❌ Error al crear línea: {str(e)}"
    
    def extruir(self, params):
        """Extruye el último perfil del sketch"""
        try:
            # Obtener el último sketch
            sketches = self.rootComp.sketches
            if sketches.count == 0:
                return "⚠️ No hay sketches para extruir"
            
            sketch = sketches.item(sketches.count - 1)
            profile = sketch.profiles.item(0)
            
            # Crear extrusion
            extrudes = self.rootComp.features.extrudeFeatures
            distance = params.get('distance', 10) / 10  # mm a cm
            
            extInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            distanceValue = adsk.core.ValueInput.createByReal(distance)
            extInput.setDistanceExtent(False, distanceValue)
            
            extrude = extrudes.add(extInput)
            
            return f"✅ Extrusión de {params.get('distance', 10)}mm completada"
            
        except Exception as e:
            return f"❌ Error al extruir: {str(e)}"
    
    def revolucion(self, params):
        """Crea una revolución"""
        return "⚠️ Revolución aún no implementada"
    
    def redondeo(self, params):
        """Crea un redondeo (fillet)"""
        return "⚠️ Redondeo aún no implementado"
    
    def chaflan(self, params):
        """Crea un chaflán"""
        return "⚠️ Chaflán aún no implementado"
