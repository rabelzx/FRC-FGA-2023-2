var socket = io.connect(
    "http://" + document.domain + ":" + location.port
  );
  var clientId;

  socket.on("connect", function () {
    // No need to set clientId here; the server will send the correct ID
  });

  socket.on("users", function (data) {
    var ul = document.getElementById("users");
    ul.innerHTML = "";
    data.clients.forEach(function (client) {
      var li = document.createElement("li");
      li.appendChild(
        document.createTextNode(`${client.id} entrou no chat`)
      );
      ul.appendChild(li);
    });
  });

  socket.on("users", function (data) {
    var ul = document.getElementById("online-users");
    ul.innerHTML = "";
    data.clients.forEach(function (client) {
      var li = document.createElement("li");
      li.appendChild(document.createTextNode(`${client.id}`));
      ul.appendChild(li);
    });
  });

  socket.on("");

  socket.on("message", function (data) {
    var ul = document.getElementById("messages");
    var li = document.createElement("li");
    li.appendChild(
      document.createTextNode(`${data.username}: ${data.message}`)
    );
    ul.appendChild(li);
  });

  function sendMessage() {
    var messageInput = document.getElementById("message_input");
    var message = messageInput.value;
    if (message.trim() !== "") {
      socket.emit("message", { message: message });
      messageInput.value = "";
    }
  }

  function changeRoom(channel) {
    var listItems = document.querySelectorAll(".left ul li");
    listItems.forEach(function (item) {
      item.classList.remove("selected");
    });

    var selectedListItem = document.querySelector(
      `.left ul li[value="${channel}"]`
    );
    selectedListItem.classList.add("selected");

    socket.emit("join_room", { room: channel });
  }