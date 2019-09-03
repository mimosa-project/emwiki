function editButtonClicked(target){
    target.form.querySelector("div[name='editBlock']").style.display = "block";
    target.style.display = 'none';
}

function cancelButtonClicked(target){
    target.form.querySelector("div[name='editBlock']").style.display = "none";
    target.form.edit.style.display = "inline";
}