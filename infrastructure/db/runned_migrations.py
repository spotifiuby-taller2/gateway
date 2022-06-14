# Los métodos que en mongo van con camelCase, acá van con snake_case

# Estos son ejemplos. Si se quieren ejecutar ponerlos en el método run_migrations de migrations.py


connection.insert_one({"name": "backoffice",
                       "apiKey": "645d293cdffe45a8674aa17b58157181a1a3127c3db705d9021307b678e7856b",
                       "active": "true",
                       "creationDate": "30/5/2022",
                       "description": "localhost:4480"})

connection.insert_one({"name": "payments",
                       "apiKey": "f91eb70d3992147cf2b1552f47adb9ef5da778923ced5ff41fba592b3c9e2a15",
                       "active": "true",
                       "creationDate": "30/5/2022",
                       "description": "localhost:4484"})

connection.insert_one({"name": "frontend auth aux",
                       "apiKey": "735e4fd4ce022f775285b8760cd053388bba04e926a5987585f89fb8f21b235f",
                       "active": "true",
                       "creationDate": "30/5/2022",
                       "description": "localhost:4482"})

connection.insert_one({"name": "media",
                       "apiKey": "938187f0c06221997960c36a7a85a30b2da2cb6e9a91962287a278c4ac1c7f8a",
                       "active": "true",
                       "creationDate": "30/5/2022",
                       "description": "localhost:4485"})

connection.insert_one({"name": "users",
                       "apiKey": "72b60f6945b9beccf2a92c7da5f5c1963f4ec68240a1814b4ec5273cac5e7a44",
                       "active": "true",
                       "creationDate": "30/5/2022",
                       "description": "localhost:4481"})

connection.insert_one({"name": "app",
                       "apiKey": "13a6bcee5bd256b05e451bde47f45a68e8bee660777f349f15f493b2873999de",
                       "active": "true",
                       "creationDate": "30/5/2022",
                       "description": "App de android"})
