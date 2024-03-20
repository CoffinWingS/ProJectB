mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"embittered1747@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\D
port = $PORT\n\
" > ~/.streamlit/config.toml
