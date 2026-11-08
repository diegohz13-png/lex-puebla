# Lex Puebla

Texto de leyes, reglamentos y demás ordenamientos del Estado Libre y Soberano de Puebla y del Municipio de Tehuacán en Markdown, convertido de las versiones publicadas por el Orden Jurídico Poblano (ojp.puebla.gob.mx), el Congreso del Estado y el Periódico Oficial del Estado de Puebla.

Complementa al repositorio de leyes federales Lex MX (https://github.com/ingteranalvarez/lex-mx) y sigue su mismo formato.

## Advertencia

Este repositorio no es una fuente oficial. Cada archivo indica la fecha de la última reforma que contiene su fuente y un campo `vigencia`:

- `actualizada`: versión vigente publicada por el Orden Jurídico Poblano al momento de cargarla (noviembre de 2026).
- `desactualizada`: se sabe que existen reformas posteriores que el texto no incluye. No debe citarse como texto vigente.
- `por verificar`: no se ha confirmado que no existan reformas posteriores.
- `abrogada`: el ordenamiento fue sustituido por otro; sólo sirve para actos celebrados durante su vigencia.
- `no vigente`: el ordenamiento ya no rige (por ejemplo, una ley de ingresos de un ejercicio fiscal concluido).

Antes de fundar un escrito en un artículo, verifique su redacción y vigencia contra el Periódico Oficial del Estado de Puebla.

## Estructura

| Carpeta | Contenido |
|---|---|
| `leyes/` | Constitución, códigos y leyes del Estado de Puebla |
| `municipal/tehuacan/` | Ley de Ingresos, reglamentos y manuales del Municipio de Tehuacán |
| `acuerdos/` | Acuerdos y actos publicados en el Periódico Oficial del Estado |
| `universitaria/buap/` | Estatuto y reglamentos de la Benemérita Universidad Autónoma de Puebla |

`catalog.json` contiene una entrada por archivo con su sigla, ruta, título, fecha de última reforma, vigencia y fuente.

## Formato

Cada archivo inicia con un encabezado YAML:

```yaml
---
type: ley-estatal
estado: Puebla
sigla: CCEP
slug: Codigo-Civil-Puebla
titulo: "Código Civil para el Estado Libre y Soberano de Puebla"
ultima_reforma: "2026-07-28"
vigencia: "actualizada"
fuente: "Orden Jurídico Poblano"
articulos: 3594
---
```

Libros y títulos van como `##`, capítulos como `###` y secciones como `####`. Cada artículo inicia con `**Artículo N.**`. Las notas de reforma de la fuente aparecen junto al artículo como `*[Nota: Artículo reformado el ...]*`. Se omiten la tabla de reformas y el índice de la fuente.
