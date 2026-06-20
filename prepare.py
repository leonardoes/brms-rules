import zipfile
import os
import glob

# Nome do arquivo JAR
jar_file = 'brms-GlobalvidaCotacao.jar'

# Caminho para o arquivo XML no arquivo JAR
xml_file_in_jar = 'BOOT-INF/classes/log4j2-spring.xml'

# Nome do novo arquivo XML que você deseja escrever
new_xml_file = 'log4j2-spring.xml'

# Encontra o arquivo .jar na pasta atual e renomeia para 'brms-SaudeCotacao.jar'
existing_jars = glob.glob("*.jar")
if existing_jars:
    os.rename(existing_jars[0], jar_file)

# Encontra e apaga o arquivo .zip na pasta atual
existing_zips = glob.glob("*.zip")
for zip_file in existing_zips:
    os.remove(zip_file)

# Crie um novo arquivo ZIP temporário para manter as alterações
temp_jar_file = 'temp.jar'
with zipfile.ZipFile(jar_file, 'r') as jar:
    with zipfile.ZipFile(temp_jar_file, 'w') as temp_jar:
        # Copie todos os arquivos do arquivo JAR original para o novo,
        # exceto o arquivo XML que você deseja substituir
        for item in jar.infolist():
            if item.filename != xml_file_in_jar:
                data = jar.read(item.filename)
                temp_jar.writestr(item, data)

        # Adicione o novo arquivo XML ao arquivo JAR
        temp_jar.write(new_xml_file, xml_file_in_jar)

# Substitua o arquivo JAR original pelo novo
os.replace(temp_jar_file, jar_file)
