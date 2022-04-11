document.addEventListener("DOMContentLoaded", (event) => {
	//ignition status
	const ignitionStatus = document.getElementById("ignitionStatus");

	//starting/stopping ignition
	const startIgnition = document.getElementById("startIgnitionBtn");
	startIgnition.addEventListener("click", () => {
		fetch("api/start_ignition").then(res => {
			return res.json();
		}).then(data => {
			console.log(data);
			ignitionStatus.innerHTML = data.message;
		}).catch(err => console.log(err));
	});

	const stopIgnition = document.getElementById("stopIgnitionBtn");
	stopIgnition.addEventListener("click", () => {
		fetch("api/stop_ignition").then(res => {
			return res.json();
		}).then(data => {
			console.log(data);
			ignitionStatus.innerHTML = data.message;
		}).catch(err => console.log(err));
	});

	//for the logs here
	const startLogging = document.getElementById("startLoggingBtn");
	startLogging.addEventListener("click", () => {
		fetch("api/start_logging").then(res => {
			return res.json();
		}).then(data => {
			console.log(data);
			ignitionStatus.innerHTML = data.message;
		}).catch(err => console.log(err));
	});

	const stopLogging = document.getElementById("stopLoggingBtn");
	stopLogging.addEventListener("click", () => {
		fetch("api/stop_logging").then(res => {
			return res.json();
		}).then(data => {
			console.log(data);
			ignitionStatus.innerHTML = data.message;
		}).catch(err => console.log(err));
	});
	//add iframe chart here
});

/* TODO
 * Change styles with change in ignition status
 * starting logging should be done in the backend when ignition starts/stops
 * add chart
 */
