# 📋 DOCTRAC - CONFIGURACIÓN DE CATEGORIZACIÓN

## 🎯 **Nuevo Sistema de Categorización Implementado**

### ⚙️ **Configuración de Tipo de Uso**

El sistema ahora soporta dos modos de funcionamiento:

#### 👤 **Modo Personal**
```bash
python manage.py setup_usage_type personal
```
- **Flujo de categorización**:
  1. 👤 **Persona/Empresa**
  2. 🏷️ **Categoría** 
  3. 📄 **Tipo de Documento**

- **Entidades disponibles**:
  - 👤 Personas (individuos)
  - 🏢 Empresas (organizaciones externas)

#### 🏢 **Modo Empresa**
```bash
python manage.py setup_usage_type empresa
```
- **Flujo de categorización**:
  1. 🏢 **Departamento** (interno) o 🏭 **Empresa** (externa)
  2. 🏷️ **Categoría**
  3. 📄 **Tipo de Documento**

- **Entidades disponibles**:
  - 🏢 Departamentos internos (Finanzas, RRHH, Ventas, etc.)
  - 🏭 Empresas externas (proveedores, clientes, etc.)

### 🚀 **Scripts de Inicio**

#### **Inicio Básico**
```bash
./start.sh
```

#### **Inicio con Configuración** (Recomendado)
```bash
./start_configured.sh
```
*Permite elegir modo de uso al inicio*

### 🔧 **Comandos de Gestión**

#### **Configurar Tipo de Uso**
```bash
# Cambiar a modo personal
python manage.py setup_usage_type personal

# Cambiar a modo empresa  
python manage.py setup_usage_type empresa
```

#### **Crear Entidades de Ejemplo**
```bash
python manage.py create_sample_entities
```
*Crea departamentos (modo empresa) o personas (modo personal)*

#### **Sincronización de Documentos**
```bash
# Manual
python manage.py sync_documents

# Dashboard de control
./doctrac_dashboard.sh

# Script automático mejorado
./sync_documents_enhanced.sh
```

### 📊 **Estado Actual del Sistema**

- ✅ **65 documentos** procesados
- ✅ **8 departamentos internos** (modo empresa)
- ✅ **8 empresas externas** configuradas
- ✅ **Automatización activa** cada 5 minutos
- ✅ **Configuración flexible** personal/empresa

### 🎯 **Flujo de Trabajo Recomendado**

1. **Configurar tipo de uso** según necesidad
2. **Crear entidades** (departamentos o personas)
3. **Procesar documentos pendientes** con nuevo flujo
4. **Categorizar** en orden: Departamento → Categoría → Tipo

### 📝 **Ejemplos de Uso**

#### **Modo Empresa - Documento de Factura**
1. 🏢 **Departamento**: Finanzas
2. 🏷️ **Categoría**: Facturas  
3. 📄 **Tipo**: Factura de Proveedor

#### **Modo Personal - Documento Médico**
1. 👤 **Persona**: Dr. Juan Pérez
2. 🏷️ **Categoría**: Salud
3. 📄 **Tipo**: Consulta Médica

### 🔄 **Cambio de Configuración en Vivo**

El sistema permite cambiar entre modos sin perder datos:
- Los departamentos se mantienen
- Las personas se conservan  
- Los documentos no se ven afectados
- Solo cambia la interfaz de categorización

---

## 🏆 **¡Sistema Completamente Configurado y Flexible!**

**Urls importantes:**
- 🌐 **Web**: http://127.0.0.1:8000/
- 📱 **Dashboard**: `./doctrac_dashboard.sh`
- ⚙️ **Configuración**: `./start_configured.sh`