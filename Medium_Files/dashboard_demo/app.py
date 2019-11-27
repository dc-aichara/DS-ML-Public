import dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash('Cryptocurrency Indicators Dashboard', external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True

