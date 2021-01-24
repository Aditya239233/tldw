async function getSummary(video_id) {
	let percentage = document.getElementById('slider').value / 100;
	let summary = await fetch(
		`https://tldw-backend.herokuapp.com/summarize?video_id=${video_id}&percentage=${percentLengthOfSummary}`,
		{
			method: 'GET',
		}
	).catch((error) => {
		document.getElementById('messages').innerHTML = error;
	});
	let summary_json = await summary.json();
	if ('error' in summary_json)
		document.getElementById('messages').innerHTML = summary_json['error'];
	else {
		document.getElementById('messages').innerHTML = 'Summary generated!';

		chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
			chrome.tabs.sendMessage(
				tabs[0].id,
				{ summary: summary_json },
				function (response) {}
			);
		});
	}
}

let summaryButton = document.getElementById('summaryButton');
summaryButton.onclick = () => {
	chrome.tabs.getSelected(null, function (tab) {
		let url = tab.url;
		if (url.indexOf('youtube.com/watch') != -1) {
			video_id = url.split('?v=')[1].substring(0, 11);
			document.getElementById('messages').innerHTML = 'Loading summary...';
			getSummary(video_id);
		} else {
			document.getElementById('messages').innerHTML = 'No youtube video found';
		}
	});
};
