import streamlit as st
import platform
import tempfile
import os
import py3Dmol
import streamlit.components.v1 as components
import subprocess
import sys



# Set page config
st.set_page_config(page_title='A web app (GUI) for Cube Toolz', layout='wide', page_icon="🧊",
menu_items={
         'About': "A web app to help you process CUBE files generated by quantum chemistry programs. Powered by [CUBE TOOLZ](https://github.com/funkymunkycool/Cube-Toolz/tree/master)"
     })

# Sidebar stuff
st.sidebar.write('# About')
st.sidebar.write(' Made By [Manas Sharma](https://manas.bragitoff.com)')
st.sidebar.write('### *Powered by*')
st.sidebar.write('* [Cube Toolz](https://github.com/funkymunkycool/Cube-Toolz/tree/master) for manipulating and processing cube files')
st.sidebar.write('* [Py3Dmol](https://3dmol.csb.pitt.edu/) for Cube File Visualizations')
st.sidebar.write('* [Streamlit](https://streamlit.io/) for making of the Web App')
# st.sidebar.write('* [PyMatgen](https://pymatgen.org/) for Periodic Structure Representations')
# st.sidebar.write('* [PubChempy](https://pypi.org/project/PubChemPy/1.0/) for Accessing the PubChem Database')
# st.sidebar.write('* [ASE](https://wiki.fysik.dtu.dk/ase/) for File Format Conversions')
st.sidebar.write('### *Source Code*')
st.sidebar.write('[GitHub Repository](https://github.com/manassharma07/CubeSuite)')

def display_cube_file(file_content_text, viz1_html_name, isovalue, opacity):
   

    # Py3Dmol visualization code
    spin = st.checkbox('Spin', value=False, key='key' + 'viz1.html')
    view = py3Dmol.view(width=500, height=400)
    view.addModel(file_content_text, 'cube')
    view.setStyle({'sphere': {'colorscheme': 'Jmol', 'scale': 0.3}, 'stick': {'colorscheme': 'Jmol', 'radius': 0.2}})
    view.addUnitCell()

    # Negative lobe
    view.addVolumetricData(file_content_text, 'cube', {'isoval': -abs(isovalue), 'color': 'blue', 'opacity': opacity})

    # Positive lobe
    view.addVolumetricData(file_content_text, 'cube', {'isoval': abs(isovalue), 'color': 'red', 'opacity': opacity})

    view.zoomTo()
    view.spin(spin)
    view.setClickable({'clickable': 'true'})
    view.enableContextMenu({'contextMenuEnabled': 'true'})
    view.show()
    view.render()

    t = view.js()
    f = open(viz1_html_name, 'w')
    f.write(t.startjs)
    f.write(t.endjs)
    f.close()

    HtmlFile = open(viz1_html_name, 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height=300, width=500)
    HtmlFile.close()



# Main app
# st.header('Cube Suite')
# st.write('##### A web app to help you process CUBE files generated by quantum chemistry programs. Powered by [CUBE TOOLZ](https://github.com/funkymunkycool/Cube-Toolz/tree/master).')

st.write('### Translate a CUBE file')

# File uploader
uploaded_file = st.file_uploader("Choose a .cub or .cube file", type=[".cub", ".cube"])

if uploaded_file is not None:
    # Read the file content as text
    file_content_text = uploaded_file.read().decode()

    temp_dir = tempfile.mkdtemp()
    filepath = os.path.join(temp_dir, uploaded_file.name)
    with open(filepath, "wb") as f:
            f.write(uploaded_file.getvalue())
    col1, col2, col3 = st.columns(3)
    x_translation = col1.number_input('X Translation', -100.0, 100.0, 0.0, 1.0)
    y_translation = col2.number_input('Y Translation', -100.0, 100.0, 0.0, 1.0)
    z_translation = col3.number_input('Z Translation', -100.0, 100.0, 0.0, 1.0)

    translate_button = st.button("Translate CUBE File")

    if translate_button:
        result = subprocess.run(["cube_tools", "-t", str(x_translation), str(y_translation), str(z_translation), filepath], capture_output=True, text=True)
        if result.stderr:
            st.write("Error:", result.stderr)
        else:
            translated_file_path = "translate.cube"
            with open(translated_file_path, 'r') as f:
                translated_file_content = f.read()

            st.download_button(
                label="Download translated CUBE file",
                data=translated_file_content,
                file_name="translated.cube",
                mime="chemical/x-cube",
            )

