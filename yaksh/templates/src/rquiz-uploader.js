/**
 * function to send something to a server using AJAX and POST method
 *
 * @param Object
 */
window.rQuizUploader = function (params) {
	var p = "",
		post = "",
		// modify path to your response logic
		url = "/absolute/path/to/rquiz-response.php",
		x = new XMLHttpRequest();

	for (p in params) {

		// exclude callback function from POSTed data
		if (typeof params[p] != "function") {
			post += p + "=" + encodeURIComponent(params[p]) + "&";
		}
	}

	x.open("POST", url, true);

	// necessary for AJAX calls using POST method
	x.setRequestHeader(
		"Content-type",
		"application/x-www-form-urlencoded"
	);

	// what to do when finished?
	x.onreadystatechange = function () {

		if (x.readyState == 4 // finished
			// we have a usable callback function?
			&& typeof params.callback == "function"
		) {
			params.callback(
				x.status == 200
				? x.responseText
				: "{}"
			);
		}
	};

	x.send(
		// remove trailing ampersand
		post.replace(/&$/, "")
	);
};
