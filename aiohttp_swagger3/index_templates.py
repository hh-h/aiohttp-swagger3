import string

SWAGGER_UI_TEMPLATE = string.Template(
    """
<!-- HTML for static distribution bundle build -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Swagger UI</title>
    <link rel="stylesheet" type="text/css" href="./swagger_ui_static/swagger-ui.css" >
    <link rel="icon" type="image/png" href="./swagger_ui_static/favicon-32x32.png" sizes="32x32" />
    <link rel="icon" type="image/png" href="./swagger_ui_static/favicon-16x16.png" sizes="16x16" />
    <style>
      html
      {
        box-sizing: border-box;
        overflow: -moz-scrollbars-vertical;
        overflow-y: scroll;
      }

      *,
      *:before,
      *:after
      {
        box-sizing: inherit;
      }

      body
      {
        margin:0;
        background: #fafafa;
      }
    </style>
  </head>

  <body>
    <div id="swagger-ui"></div>

    <script src="./swagger_ui_static/swagger-ui-bundle.js"> </script>
    <script src="./swagger_ui_static/swagger-ui-standalone-preset.js"> </script>
    <script>
    window.onload = function() {
      // Begin Swagger UI call region
      const ui = SwaggerUIBundle({...{
        url: "./swagger.json",
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset
        ],
        plugins: [
          SwaggerUIBundle.plugins.DownloadUrl
        ],
        layout: "StandaloneLayout"
      }, ...${settings}});
      // End Swagger UI call region

      window.ui = ui
    }
  </script>
  </body>
</html>
"""
)

REDOC_UI_TEMPLATE = string.Template(
    """
<!DOCTYPE html>
<html>
  <head>
    <title>ReDoc</title>
    <!-- needed for adaptive design -->
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="./redoc_ui_static/google-fonts.css" >
    <link rel="shortcut icon" href="./redoc_ui_static/favicon.ico"/>
    <link rel="icon" type="image/png" sizes="16x16" href="./redoc_ui_static/favicon-16x16.png"/>
    <link rel="icon" type="image/png" sizes="32x32" href="./redoc_ui_static/favicon-32x32.png"/>

    <!--
    ReDoc doesn't change outer page styles
    -->
    <style>
      body {
        margin: 0;
        padding: 0;
      }
    </style>
  </head>
  <body>
    <div id='redoc-ui'></div>
    <script src="./redoc_ui_static/redoc.standalone.js"> </script>
    <script>
        Redoc.init('./swagger.json', ${settings}, document.getElementById('redoc-ui'))
    </script>
  </body>
</html>
"""
)
