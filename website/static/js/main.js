function deletePerson() {
    fetch('/delete-person', {
        method: 'POST'
    })
    .then((res) => window.location.reload()
    );
};

function deleteResult(draw){
	fetch("/delete-result", {
		method: "POST",
		body: JSON.stringify(draw)
	}).then((res) => window.location.reload())
		}

function submitResult(result){
    fetch("/submit-result", {
        method: "POST",
        body: JSON.stringify(result)
    }).then((res) => window.location.assign("/submit-sending-email"))
}
