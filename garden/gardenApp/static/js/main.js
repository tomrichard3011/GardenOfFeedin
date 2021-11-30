// update file name after uploading a file
// idea: https://stackoverflow.com/questions/572768/styling-an-input-type-file-button
$('#myfile').bind('change', function() { 
	var fileName = ''; 
	fileName = $(this).val(); 
	var span = document.getElementById("file-selected");
//	$('#file-selected').innerHTML(fileName); 
	var typeOut = fileName.split("\\").pop();	// https://stackoverflow.com/questions/1804745/get-the-filename-of-a-fileupload-in-a-document-through-javascript
	if (typeOut == "") typeOut = "No file selected";
	span.innerHTML = typeOut;
	//console.log(fileName);
})
