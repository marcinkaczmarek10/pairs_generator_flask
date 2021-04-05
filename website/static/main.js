function deleteResult(resultId){
	fetch('/delete-result', {
		method: 'POST',
		body: JSON.stringify({result_id: resultId})
	}).then((_res) => {
		window.location.href = "/show-results";
	})
}