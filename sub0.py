import streamlit as st
import streamlit.components.v1 as components

st.title('Streamlit component for molecular visualization')
st.write('This component is currently a static version using 3Dmol.js for visualization. It allows to upload pdb files.')
components.html('''


<script src="https://3Dmol.csb.pitt.edu/build/3Dmol-min.js"></script>


        <form enctype="multipart/form-data" >
            <input id="ligand" type="file" />
        </form>


<script>
	var glviewer = null;
	var labels = [];


	
	var colorSS = function(viewer) {
		//color by secondary structure
		var m = viewer.getModel();
		m.setColorByFunction({}, function(atom) {
			if(atom.ss == 'h') return "magenta";
			else if(atom.ss == 's') return "orange";
			else return "white";
		});
		viewer.render();
	}

	var atomcallback = function(atom, viewer) {
		if (atom.clickLabel === undefined
				|| !atom.clickLabel instanceof $3Dmol.Label) {
			atom.clickLabel = viewer.addLabel(atom.elem + atom.serial, {
				fontSize : 14,
				position : {
					x : atom.x,
					y : atom.y,
					z : atom.z
				},
				backgroundColor: "black"
			});
			atom.clicked = true;
		}

		//toggle label style
		else {

			if (atom.clicked) {
				var newstyle = atom.clickLabel.getStyle();
				newstyle.backgroundColor = 0x66ccff;

				viewer.setLabelStyle(atom.clickLabel, newstyle);
				atom.clicked = !atom.clicked;
			}
			else {
				viewer.removeLabel(atom.clickLabel);
				delete atom.clickLabel;
				atom.clicked = false;
			}

		}
	};
            var readText = function(input,func) {
			if(input.files.length > 0) {
				var file = input.files[0];
				var reader = new FileReader();
			    reader.onload = function(evt) {
			    	func(evt.target.result,file.name);
			    };
			    reader.readAsText(file);
			    $(input).val('');
			}
		};


		
	$(document).ready(function() {

		moldata = data = $("#ligand").val();
		glviewer = $3Dmol.createViewer("gldiv", {
			defaultcolors : $3Dmol.rasmolElementColors
		});
		glviewer.setBackgroundColor(0xffffff);

		receptorModel = m = glviewer.addModel(data, "pqr");

		atoms = m.selectedAtoms({});

		for ( var i in atoms) {
			var atom = atoms[i];
			atom.clickable = true;
			atom.callback = atomcallback;
		}

		glviewer.mapAtomProperties($3Dmol.applyPartialCharges);
		glviewer.zoomTo();
		glviewer.render();


	});
</script>
</head>

<body>


        
        
	<div id="gldiv" style="width: 100%; height: 40vh; margin: 0; padding: 0; border: 0;"></div>

	<hr style="margin: 0;">

	<br>
	Set structure Identifier (For example 6VXX) and click download:

	
	<input id="pdbid" value="6VXX" size=4>
        <button
		onclick="glviewer.clear(); m = $3Dmol.download('pdb:' + $('#pdbid').val(), glviewer, {doAssembly:true, noSecondaryStructure: false});">Download</button>

	<br>

	or upload local file <input type="file" onchange="readText(this, function(data, name) {glviewer.clear(); m= glviewer.addModel(data,name); glviewer.zoomTo(); glviewer.render();} );">
        <br>
        <hr>
	<br>
        <p style="font-size:22px;">Customize visualization:</p>
	

        For small molecules
	
	<input type="button" value="Stick"
		onclick="glviewer.setStyle({},{stick:{}}); glviewer.render();"></input>
	


	<input type="button" value="Sphere"
		onclick="glviewer.setStyle({},{sphere:{}}); glviewer.render();"></input>
	<br>

        For proteins  
	
	<input type="button" value="Cartoon"
		onclick="glviewer.setStyle({hetflag:false},{cartoon:{}}); glviewer.render();"></input>
	

	<input type="button" value="Color SS"
		onclick="colorSS(glviewer);"></input>




</body>



''',width=800,height=800)

