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
st.sidebar.write('Originally Made By [Manas Sharma](https://manas.bragitoff.com)')
st.sidebar.write('### *Powered by*')
st.sidebar.write('* [Cube Toolz](https://github.com/funkymunkycool/Cube-Toolz/tree/master) for manipulating and processing cube files')
st.sidebar.write('* [Py3Dmol](https://3dmol.csb.pitt.edu/) for Cube File Visualizations')
st.sidebar.write('* [Streamlit](https://streamlit.io/) for making of the Web App')
# st.sidebar.write('* [PyMatgen](https://pymatgen.org/) for Periodic Structure Representations')
# st.sidebar.write('* [PubChempy](https://pypi.org/project/PubChemPy/1.0/) for Accessing the PubChem Database')
# st.sidebar.write('* [ASE](https://wiki.fysik.dtu.dk/ase/) for File Format Conversions')
st.sidebar.write('### *Contributors*')
st.sidebar.write('[Ya-Fan Chen ](https://github.com/Lexachoc)')
st.sidebar.write('### *Source Code*')
st.sidebar.write('[GitHub Repository](https://github.com/manassharma07/Cube_Suite)')

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


# New feature since streamlit v1.33.0
@st.experimental_fragment
def show_download_button(subtracted_file_content):
    st.download_button(
        label="Download subtracted CUBE file",
        data=subtracted_file_content,
        file_name="diff.cube",
        mime="chemical/x-cube",
    )


# Main app
# st.header('Cube Suite')
# st.write('##### A web app to help you process CUBE files generated by quantum chemistry programs. Powered by [CUBE TOOLZ](https://github.com/funkymunkycool/Cube-Toolz/tree/master).')

st.write('### Subtract Two CUBE Files')

# File uploaders
uploaded_file1 = st.file_uploader("Choose the first .cub or .cube file", type=[".cub", ".cube"])
uploaded_file2 = st.file_uploader("Choose the second .cub or .cube file", type=[".cub", ".cube"])

if uploaded_file1 is not None and uploaded_file2 is not None:
    # Read the file contents as text
    file_content_text1 = uploaded_file1.read().decode()
    file_content_text2 = uploaded_file2.read().decode()

    temp_dir = tempfile.mkdtemp()
    filepath1 = os.path.join(temp_dir, uploaded_file1.name)
    filepath2 = os.path.join(temp_dir, uploaded_file2.name)

    with open(filepath1, "wb") as f:
        f.write(uploaded_file1.getvalue())
    with open(filepath2, "wb") as f:
        f.write(uploaded_file2.getvalue())

    add_button = st.button("Subtract CUBE Files")

    if add_button:
        result = subprocess.run(["cube_tools", "-s", filepath1, filepath2], capture_output=True, text=True)
        if result.stderr:
            st.write("Error:", result.stderr)
        else:
            subtracted_file_path = "diff.cube"
            with open(subtracted_file_path, 'r') as f:
                subtracted_file_content = f.read()

            show_download_button(subtracted_file_content)

