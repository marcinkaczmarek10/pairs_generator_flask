function deleteResult(resultId){
	fetch('/delete-result', {
		method: 'POST',
		body: JSON.stringify({resultId: resultId})
	}).then((_res) => {
		window.location.href = "/show-results";
	})
}