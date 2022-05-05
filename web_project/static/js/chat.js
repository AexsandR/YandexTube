async function getMessages(user_id, chat_id) {
    var xhr = new XMLHttpRequest();  // подключение для получения GET-запроса
    xhr.open("POST", "/api/get/messages", true);  // создаём ассинхронное соединение с сервером
    xhr.setRequestHeader("Content-Type", "application/json");  // задаём заголовок

    // Setting the function to get the values
    xhr.onreadystatechange = function () {
        // Messages are fully received
        if (xhr.readyState === 4 && xhr.status === 200) {
            var json = JSON.parse(xhr.responseText);

            if (json.status === 200 && json.content.length !== 0) {
                var content = json.content;
                var chat = document.getElementById("chat");  // getting the chat element

                for (value of content) {
                    // Message generation
                    if (value.id <= lastMessageId)
                        // Fixing the message replay bug
                        continue;

                    if (value.owner === user_id) {
                        // Me
                        if (value.text.trim().startsWith("[") && value.text.trim().endsWith("]")) {
                            // Unusual elements
                            command = value.text.trim().slice(1, -1).trim();

                            if (command.toLowerCase().startsWith("img") && command.slice(3).trim().toLowerCase().startsWith("link=")) {
                                // Image
                                command = command.slice(3).trim().slice(5).trim()  // link of the image
                                var message = document.createElement("div");  // <div> </div>
                                message.classList.add("outer-container");  // <div class="outer-container"> </div>
                                message.style = "min-width: 0; min-height: 20rem; max-height: 100%;";  // <div class="outer-container" style="..."> </div>

                                var messageContent = "<div class=\"avatar\"> </div>";
                                messageContent += "<div class=\"inner-container\">";
                                messageContent += "    <div class=\"spacer\"> </div>";
                                messageContent += "    <div class=\"bubble me\" style=\"padding: 0.1rem;\">";
                                messageContent += "        <a href=" + command + " target=\"_blank\">";
                                messageContent += "            <img class=\"image\" src=" + command + " alt=\"\" width=\"100%\" height=\"100%\">";
                                messageContent += "        </a>";
                                messageContent += "    </div>";
                                messageContent += "</div>";

                                message.innerHTML = messageContent;

                                chat.prepend(message);
                            } else if (command.toLowerCase().startsWith("alert")) {
                                // Alert
                                command = command.slice(5).trim();

                                var message = document.createElement("div");
                                message.classList.add("alert");

                                if (command.toLowerCase().startsWith("type=")) {
                                    command = command.slice(5).trim()

                                    if (command.toLowerCase().startsWith("primary")) {
                                        message.classList.add("alert-primary");
                                    } else if (command.toLowerCase().startsWith("info")) {
                                        message.classList.add("alert-info");
                                    } else if (command.toLowerCase().startsWith("success")) {
                                        message.classList.add("alert-success");
                                    } else if (command.toLowerCase().startsWith("warning")) {
                                        message.classList.add("alert-warning");
                                    } else if (command.toLowerCase().startsWith("danger")) {
                                        message.classList.add("alert-danger");
                                    } else {
                                        message.classList.add("alert-info");
                                    }
                                    command = command.slice(command.split(' ')[0].length).trim()
                                } else {
                                    message.classList.add("alert-info");
                                }
                                message.innerHTML = command;

                                chat.prepend(message);
                            } else if (command.toLowerCase().startsWith("card")) {
                                // Card
                                command = command.slice(5).trim().split("\"");
                                command = command.map(function (element) {return element.trim()});
                                command = command.filter(function (element) {return element != ''});

                                var parameters = {title: "Card title", link: "#"};

                                for (var index = 0; index < command.length; index++) {
                                    if (command[index].endsWith("=")) {
                                        if (command[index].slice(0, -1).trim().toLowerCase() === "image") {
                                            if (command[index + 1] !== undefined) {
                                                parameters.image = command[index + 1];
                                            }
                                        } else if (command[index].slice(0, -1).trim().toLowerCase() === "title") {
                                            if (command[index + 1] !== undefined) {
                                                parameters.title = command[index + 1];
                                            }
                                        } else if (command[index].slice(0, -1).trim().toLowerCase() === "text") {
                                            if (command[index + 1] !== undefined) {
                                                parameters.text = command[index + 1];
                                            }
                                        } else if (command[index].slice(0, -1).trim().toLowerCase() === "button") {
                                            if (command[index + 1] !== undefined) {
                                                parameters.button = command[index + 1];
                                            }
                                        } else if (command[index].slice(0, -1).trim().toLowerCase() === "link") {
                                            if (command[index + 1] !== undefined) {
                                                parameters.link = command[index + 1];
                                            }
                                        }
                                    }
                                }

                                var message = document.createElement("div");
                                message.style = "margin-bottom: 0.1rem;";
                                var messageContent = "<div class=\"inner-container\" style=\"height: auto;\">";
                                messageContent += "    <div class=\"spacer\"> </div>"
                                messageContent += "    <div class=\"bubble me\" style=\"padding: 0.1rem;max-width: 40%;\">";
                                messageContent += "        <div class=\"card image\" style=\"width: 100%;height: 100%;\">";

                                if (parameters.image !== undefined) {
                                    messageContent += "<a href=\"" + parameters.image +"\" target=\"_blank\">";
                                    messageContent += "    <img class=\"image\" src=\"" + parameters.image + "\" alt=\"\" width=\"100%\" height=\"100%\">";
                                    messageContent += "</a>";
                                }

                                messageContent += "<div class=\"card-body\">";
                                messageContent += "    <h5 class=\"card-title\" style=\"text-align: center;\"> " + parameters.title + " </h5>";

                                if (parameters.text !== undefined) {
                                    messageContent += "<p class=\"card-text\" style=\"text-align: center;\">" + parameters.text + "</p>";
                                }

                                if (parameters.button !== undefined) {
                                    messageContent += "<a href=\"" + parameters.link + "\" class=\"btn btn-primary\" style=\"left: 50%; transform: translate(-50%, 0); width: 100%;\"> " + parameters.button + " </a>";
                                }

                                messageContent += "</div></div></div></div><div class=\"spacer\"></div>";
                                message.innerHTML = messageContent;

                                chat.prepend(message);
                            } else {
                                // Simple message
                                var message = document.createElement("div");
                                message.classList.add("outer-container");

                                var messageContent = "<div class=\"avatar\"> </div>";
                                messageContent += "<div class=\"inner-container\">";
                                messageContent += "    <div class=\"spacer\"></div>";
                                messageContent += "    <div class=\"bubble me\"> " + value.text + " </div>";
                                messageContent += "</div>";

                                message.innerHTML = messageContent;

                                chat.prepend(message);
                            }
                        } else {
                            // Simple message
                            var message = document.createElement("div");
                            message.classList.add("outer-container");

                            var messageContent = "<div class=\"avatar\"> </div>";
                            messageContent += "<div class=\"inner-container\">";
                            messageContent += "    <div class=\"spacer\"></div>";
                            messageContent += "    <div class=\"bubble me\"> " + value.text + " </div>";
                            messageContent += "</div>";

                            message.innerHTML = messageContent;

                            chat.prepend(message);
                        }
                    } else {
                        // Other users
                        if (value.text.trim().startsWith("[") && value.text.trim().endsWith("]")) {
                            // Unusual elements
                            command = value.text.trim().slice(1, -1).trim();

                            if (command.toLowerCase().startsWith("img") && command.slice(3).trim().toLowerCase().startsWith("link=")) {
                                // Image
                                command = command.slice(3).trim().slice(5).trim()  // link of the image
                                var message = document.createElement("div");  // <div> </div>
                                message.classList.add("outer-container");  // <div class="outer-container"> </div>
                                message.style = "min-width: 0; min-height: 20rem; max-height: 100%;";  // <div class="outer-container font-monospace" style="..."> </div>

                                var messageContent = "<a class=\"avatar\" href=\"/user?user=" + value.owner + "\">";
                                messageContent += "    <img src=\"/static/images/users/" + value.user_image + "\" style=\"border-radius: 50%;\" width=\"100%\" height=\"100%\" alt=\"\">";
                                messageContent += "</a>"
                                messageContent += "<div class=\"inner-container\">";
                                messageContent += "    <div class=\"bubble you\" style=\"padding: 0.1rem;\">";
                                messageContent += "        <a href=" + command + " target=\"_blank\">";
                                messageContent += "            <img class=\"image\" src=" + command + " alt=\"\" width=\"100%\" height=\"100%\">";
                                messageContent += "        </a>";
                                messageContent += "    </div>";
                                messageContent += "</div>";
                                messageContent += "<div class=\"spacer\"> </div>";

                                message.innerHTML = messageContent;

                                var chat = document.getElementById("chat");  // getting the chat element
                                chat.prepend(message);
                            } else if (command.toLowerCase().startsWith("alert")) {
                                // Alert
                                command = command.slice(5).trim();

                                var message = document.createElement("div");
                                message.classList.add("alert");

                                if (command.toLowerCase().startsWith("type=")) {
                                    command = command.slice(5).trim()

                                    if (command.toLowerCase().startsWith("primary")) {
                                        message.classList.add("alert-primary");
                                    } else if (command.toLowerCase().startsWith("info")) {
                                        message.classList.add("alert-info");
                                    } else if (command.toLowerCase().startsWith("success")) {
                                        message.classList.add("alert-success");
                                    } else if (command.toLowerCase().startsWith("warning")) {
                                        message.classList.add("alert-warning");
                                    } else if (command.toLowerCase().startsWith("danger")) {
                                        message.classList.add("alert-danger");
                                    } else {
                                        message.classList.add("alert-info");
                                    }
                                    command = command.slice(command.split(' ')[0].length).trim();
                                } else {
                                    message.classList.add("alert-info");
                                }
                                message.innerHTML = command;

                                chat.prepend(message);
                            } else if (command.toLowerCase().startsWith("card")) {
                                // Card
                                command = command.slice(5).trim().split("\"");
                                command = command.map(function (element) {return element.trim()});
                                command = command.filter(function (element) {return element != ''});

                                var parameters = {title: "Card title", link: "#"};

                                for (var index = 0; index < command.length; index++) {
                                    if (command[index].endsWith("=")) {
                                        if (command[index].slice(0, -1).trim().toLowerCase() === "image") {
                                            if (command[index + 1] !== undefined) {
                                                parameters.image = command[index + 1];
                                            }
                                        } else if (command[index].slice(0, -1).trim().toLowerCase() === "title") {
                                            if (command[index + 1] !== undefined) {
                                                parameters.title = command[index + 1];
                                            }
                                        } else if (command[index].slice(0, -1).trim().toLowerCase() === "text") {
                                            if (command[index + 1] !== undefined) {
                                                parameters.text = command[index + 1];
                                            }
                                        } else if (command[index].slice(0, -1).trim().toLowerCase() === "button") {
                                            if (command[index + 1] !== undefined) {
                                                parameters.button = command[index + 1];
                                            }
                                        } else if (command[index].slice(0, -1).trim().toLowerCase() === "link") {
                                            if (command[index + 1] !== undefined) {
                                                parameters.link = command[index + 1];
                                            }
                                        }
                                    }
                                }

                                var message = (parameters.button === undefined && parameters.link !== '#') ? document.createElement("a") : document.createElement("div");
                                message.style = "margin-bottom: 0.1rem;";
                                if (parameters.button === undefined && parameters.link !== '#') {
                                    message.href = parameters.link
                                }

                                var messageContent = "<div class=\"avatar\" style=\"margin-bottom: 0.1rem;\">";
                                messageContent += "    <a href=\"/user?user=" + value.owner + "\" target=\"_blank\">";
                                messageContent += "        <img src=\"/static/images/users/" + value.user_image + "\" style=\"border-radius: 50%;\" width=\"100%\" height=\"100%\" alt=\"\">";
                                messageContent += "    </a>"
                                messageContent += "</div>";
                                messageContent += "<div class=\"inner-container\" style=\"height: auto;\">";
                                messageContent += "    <div class=\"bubble you\" style=\"padding: 0.1rem;max-width: 40%;\">";
                                messageContent += "        <div class=\"card image\" style=\"width: 100%;height: 100%;\">";

                                if (parameters.image !== undefined) {
                                    messageContent += "<a href=\"" + parameters.image +"\" target=\"_blank\">";
                                    messageContent += "    <img class=\"image\" src=\"" + parameters.image + "\" alt=\"\" width=\"100%\" height=\"100%\">";
                                    messageContent += "</a>";
                                }

                                messageContent += "<div class=\"card-body\">";
                                messageContent += "    <h5 class=\"card-title\" style=\"text-align: center;\"> " + parameters.title + " </h5>";

                                if (parameters.text !== undefined) {
                                    messageContent += "<p class=\"card-text\" style=\"text-align: center;\">" + parameters.text + "</p>";
                                }

                                if (parameters.button !== undefined) {
                                    messageContent += "<a href=\"" + parameters.link + "\" class=\"btn btn-primary\" style=\"left: 50%; transform: translate(-50%, 0); width: 100%;\"> " + parameters.button + " </a>";
                                }

                                messageContent += "</div></div></div></div><div class=\"spacer\"></div>";
                                message.innerHTML = messageContent;

                                chat.prepend(message);
                            } else {
                                // Simple message
                                var message = document.createElement("div");
                                message.classList.add("outer-container");

                                var messageContent = "<a class=\"avatar\" href=\"/user?user=" + value.owner + "\">";
                                messageContent += "    <img src=\"/static/images/users/" + value.user_image + "\" style=\"border-radius: 50%;\" width=\"100%\" height=\"100%\" alt=\"\">"
                                messageContent += "</div>"
                                messageContent += "<div class=\"inner-container\">";
                                messageContent += "    <div class=\"bubble me\"> " + value.text + " </div>";
                                messageContent += "</div>";
                                messageContent += "<div class=\"spacer\"></div>";

                                message.innerHTML = messageContent;

                                chat.prepend(message);
                            }
                        } else {
                            // Simple message
                            var message = document.createElement("div");
                            message.classList.add("outer-container");

                            var messageContent = "<a class=\"avatar\" href=\"/user/?user=" + value.owner + "\">";
                            messageContent += "    <img src=\"/static/images/users/" + value.user_image + "\" style=\"border-radius: 50%;\" width=\"100%\" height=\"100%\" alt=\"\">"
                            messageContent += "</a>"
                            messageContent += "<div class=\"inner-container\">";
                            messageContent += "    <div class=\"bubble me\"> " + value.text + " </div>";
                            messageContent += "</div>";
                            messageContent += "<div class=\"spacer\"></div>";

                            message.innerHTML = messageContent;

                            chat.prepend(message);
                        }
                    }
                    lastMessageId = lastMessageId < value.id ? value.id : lastMessageId;
                }
            }
        }
    }

    var data = {
                    count: 100,
                    chat_id: chat_id,
                    last_message: lastMessageId
               };
    data = JSON.stringify(data);

    xhr.send(data);
}

async function postMessage(user_id, chat_id) {
    var input = document.getElementById("input");
    var text = input.value;

    if (text.trim()) {
        var xhr = new XMLHttpRequest();  // Connection for sending a POST-request
        xhr.open("POST", "/api/send/messages", true);  // Creating an asynchronous connection with the server
        xhr.setRequestHeader("Content-Type", "application/json");  // Setting the header

        var data = {
                        type: "message",
                        content: {
                            owner: user_id,
                            chat_id: chat_id,
                            text: text
                        }
                    };
        data = JSON.stringify(data);

        xhr.send(data);  // Sending request

        input.value = '';  // Clearing the input field
    }
}
