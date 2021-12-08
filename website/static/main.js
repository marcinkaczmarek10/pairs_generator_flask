function deleteResult(draw){
	fetch("/delete-result", {
		method: "POST",
		body: JSON.stringify(draw)
	}).then((res) => console.log(res))
		}