  var socket = io.connect("http://" + document.domain + ":" + location.port);
  var clientId;

  socket.on("connect", function () {});

  socket.on("users", function (data) {
    var ul;

    console.log(data);

    if (data.room === "room1" || data.room === "room2" || data.room === "room3") {
      ul = document.getElementById(`users-${data.room}`);
      ul.innerHTML = ""; // Limpar a lista antes de adicionar usuários

      data.room_users.forEach(function (client) {
        var li = document.createElement("li");
        li.appendChild(document.createTextNode(`${client}`));
        ul.appendChild(li);
      });
    }

    var ul = document.getElementById("users");
    ul.innerHTML = "";
    data.clients.forEach(function (client) {
      var li = document.createElement("li");
      li.appendChild(document.createTextNode(`${client.id} entrou no chat`));
      ul.appendChild(li);
    });
  });
  
  socket.on("");
  socket.on("message", function (data) {
    if (data.room == "room1") {
      var ul = document.getElementById("messages-room1");
      var li = document.createElement("li");
      li.appendChild(
        document.createTextNode(`${data.username}: ${data.message}`)
      );
      ul.appendChild(li);
    } else if (data.room == "room2") {
      var ul = document.getElementById("messages-room2");
      var li = document.createElement("li");
      li.appendChild(
        document.createTextNode(`${data.username}: ${data.message}`)
      );
      ul.appendChild(li);
    } else if (data.room == "room3") {
      var ul = document.getElementById("messages-room3");
      var li = document.createElement("li");
      li.appendChild(
        document.createTextNode(`${data.username}: ${data.message}`)
      );
      ul.appendChild(li);
    }
  });

  function sendMessage() {
    var messageInput = document.getElementById("message_input");
    var message = messageInput.value;
    if (message.trim() !== "") {
      socket.emit("message", { message: message });
      messageInput.value = "";
    }
  }

  // Adiciona um ouvinte de evento de teclado ao campo de entrada de mensagem
  document
    .getElementById("message_input")
    .addEventListener("keydown", function (event) {
      // Verifica se a tecla pressionada é "Enter" (código 13)
      if (event.key === "Enter" || event.keyCode === 13) {
        sendMessage();
      }
    });

  // Adiciona um ouvinte de evento de clique ao botão "Enviar"
  document.getElementById("send_button").addEventListener("click", sendMessage);

  function joinInit(channel) {
    let listItemsInit = document.querySelectorAll(".left .init-room li");
    listItemsInit.forEach(function (item) {
      item.classList.remove("selected");
    });
    let listItemsText = document.querySelectorAll(".left .text-rooms li");
    listItemsText.forEach(function (item) {
      item.classList.remove("selected");
    });
    let listItemsVideo = document.querySelectorAll(".left .video-rooms li");
    listItemsVideo.forEach(function (item) {
      item.classList.remove("selected");
    });

    var selectedListItem = document.querySelector(
      `.left .init-room li[value="${channel}"]`
    );
    selectedListItem.classList.add("selected");

    var centerMessageElement = document.querySelector(".center-message");
    centerMessageElement.classList.toggle("active", false);

    var centerVideoElement = document.querySelector(".center-video");
    centerVideoElement.classList.toggle("active", false);

    var centerInitElement = document.querySelector(".center-init");
    centerInitElement.classList.toggle("active", false);

    var initDiv = document.querySelector(".initNone");
    initDiv.classList.toggle("active", false);

    var initUser = document.querySelector(".userNone");
    initUser.classList.toggle("active", false);

    // socket.emit("join", { theme: channel });
  }

  function changeRoom(channel) {
    let listItemsInit = document.querySelectorAll(".left .init-room li");
    listItemsInit.forEach(function (item) {
      item.classList.remove("selected");
    });
    let listItemsText = document.querySelectorAll(".left .text-rooms li");
    listItemsText.forEach(function (item) {
      item.classList.remove("selected");
    });
    let listItemsVideo = document.querySelectorAll(".left .video-rooms li");
    listItemsVideo.forEach(function (item) {
      item.classList.remove("selected");
    });

    var selectedListItem = document.querySelector(
      `.left .text-rooms li[value="${channel}"]`
    );
    selectedListItem.classList.add("selected");

    var centerVideoElement = document.querySelector(".center-message");
    centerVideoElement.classList.toggle("active", true);

    var centerVideoElement = document.querySelector(".center-video");
    centerVideoElement.classList.toggle("active", false);

    var centerInitElement = document.querySelector(".center-init");
    centerInitElement.classList.toggle("active", true);

    var initDiv = document.querySelector(".initNone");
    initDiv.classList.toggle("active", true);

    //ocultar as outras ul tambem condicionalmente
    if (channel == "room1") {
      var ul1 = document.getElementById("messages-room1");
      ul1.style.display = "block";
      var ul2 = document.getElementById("messages-room2");
      ul2.style.display = "none";
      var ul3 = document.getElementById("messages-room3");
      ul3.style.display = "none";

      ul1 = document.getElementById("users-room1");
      ul1.style.display = "block";
      ul2 = document.getElementById("users-room2");
      ul2.style.display = "none";
      ul3 = document.getElementById("users-room3");
      ul3.style.display = "none";
    }
    if (channel == "room2") {
      var ul1 = document.getElementById("messages-room1");
      ul1.style.display = "none";
      var ul2 = document.getElementById("messages-room2");
      ul2.style.display = "block";
      var ul3 = document.getElementById("messages-room3");
      ul3.style.display = "none";

      ul1 = document.getElementById("users-room1");
      ul1.style.display = "none";
      ul2 = document.getElementById("users-room2");
      ul2.style.display = "block";
      ul3 = document.getElementById("users-room3");
      ul3.style.display = "none";
    }
    if (channel == "room3") {
      var ul1 = document.getElementById("messages-room1");
      ul1.style.display = "none";
      var ul2 = document.getElementById("messages-room2");
      ul2.style.display = "none";
      var ul3 = document.getElementById("messages-room3");
      ul3.style.display = "block";

      ul1 = document.getElementById("users-room1");
      ul1.style.display = "none";
      ul2 = document.getElementById("users-room2");
      ul2.style.display = "none";
      ul3 = document.getElementById("users-room3");
      ul3.style.display = "block";
    }

    socket.emit("join_room", { room: channel });
  }

  //lógica do chat de vídeo

  //troca a sala de vídeo
  function changeVideoRoom(channel) {
    var ul1 = document.getElementById("users-room1");
    ul1.style.display = "none";
    var ul2 = document.getElementById("users-room2");
    ul2.style.display = "none";
    var ul3 = document.getElementById("users-room3");
    ul3.style.display = "none";
    
    let listItemsInit = document.querySelectorAll(".left .init-room li");
    listItemsInit.forEach(function (item) {
      item.classList.remove("selected");
    });
    let listItemsText = document.querySelectorAll(".left .text-rooms li");
    listItemsText.forEach(function (item) {
      item.classList.remove("selected");
    });
    let listItemsVideo = document.querySelectorAll(".left .video-rooms li");
    listItemsVideo.forEach(function (item) {
      item.classList.remove("selected");
    });

    var selectedListItem = document.querySelector(
      `.left .video-rooms li[value="${channel}"]`
    );
    selectedListItem.classList.add("selected");

    var centerVideoElement = document.querySelector(".center-message");
    centerVideoElement.classList.toggle("active", false);

    var centerVideoElement = document.querySelector(".center-video");
    centerVideoElement.classList.toggle("active", true);

    var centerInitElement = document.querySelector(".center-init");
    centerInitElement.classList.toggle("active", true);

    var initDiv = document.querySelector(".initNone");
    initDiv.classList.toggle("active", true);

    var initUser = document.querySelector(".userNone");
    initUser.classList.toggle("active", true);

    
  }

  //ingressa na sala de vídeo
  function joinVideoRoom() {
    var listItems = document.querySelectorAll(".left .video-rooms li");
    var room;
    listItems.forEach(function (item) {
      if (item.classList.contains("selected")) {
        room = item.getAttribute("value");
      }
    });

    socket.emit("join_video", { theme: room });

  }

  //sai da sala de vídeo
  function leaveVideoRoom() {
    var listItems = document.querySelectorAll(".left .video-rooms li");
    var room;
    listItems.forEach(function (item) {
      if (item.classList.contains("selected")) {
        room = item.getAttribute("value");
      }
    });

    socket.emit("leave_video", { theme: room });
    var centerVideoElement = document.querySelector(".center-video");
    centerVideoElement.classList.toggle("active", false);
    toggleCamera();
    toggleMute();
  }

  //liga/desliga o microfone
  function toggleMute() {
    var localVideo = document.getElementById("localVideo");
    localVideo.muted = !localVideo.muted;
  }

  //liga/desliga a câmera
  function toggleCamera() {
    var localVideo = document.getElementById("localVideo");
    var tracks = localVideo.srcObject.getVideoTracks();
    tracks.forEach((track) => (track.enabled = !track.enabled));
  }

  //recebe a resposta do join e insere o user na sala de vídeo
  socket.on("theme_joined", (theme) => {
    navigator.mediaDevices
      .getUserMedia({ video: true, audio: true })
      .then((stream) => {
        const localVideo = document.getElementById("localVideo");
        localVideo.srcObject = stream;

        const peerConnection = new RTCPeerConnection();

        stream
          .getTracks()
          .forEach((track) => peerConnection.addTrack(track, stream));

        peerConnection
          .createOffer()
          .then((offer) => peerConnection.setLocalDescription(offer))
          .then(() =>
            socket.emit("offer", {
              theme: theme,
              offer: peerConnection.localDescription,
            })
          )
          .catch((error) => console.error(error));

        peerConnection.onicecandidate = (event) => {
          if (event.candidate) {
            socket.emit("ice_candidate", {
              theme: theme,
              candidate: event.candidate,
            });
          }
        };

        socket.on("offer_received", (data) => {
          const remoteVideo = document.getElementById("remoteVideo");
          peerConnection
            .setRemoteDescription(data.offer)
            .then(() => peerConnection.createAnswer())
            .then((answer) => peerConnection.setLocalDescription(answer))
            .then(() =>
              socket.emit("answer", {
                theme: theme,
                answer: peerConnection.localDescription,
              })
            )
            .catch((error) => console.error(error));
        });

        socket.on("answer_received", (data) => {
          peerConnection
            .setRemoteDescription(data.answer)
            .catch((error) => console.error(error));
        });

        socket.on("ice_candidate_received", (data) => {
          peerConnection
            .addIceCandidate(data.candidate)
            .catch((error) => console.error(error));
        });

        peerConnection.ontrack = (event) => {
          const remoteVideo = document.getElementById("remoteVideo");
          remoteVideo.srcObject = event.streams[0];
        };
      })
      .catch((error) => console.error(error));
  });

  // recebe a resposta do leave e remove o usuário da sala de vídeo
  socket.on("theme_left", (theme) => {
    const localVideo = document.getElementById("localVideo");
    const remoteVideo = document.getElementById("remoteVideo");

    // Close the local stream
    let tracks = localVideo.srcObject.getTracks();
    tracks.forEach((track) => track.stop());

    // Close the peer connection
    if (peerConnection) {
      peerConnection.close();
      peerConnection = null;
    }

    // Clear the video elements
    localVideo.srcObject = null;
    remoteVideo.srcObject = null;

    // Update UI or perform any other cleanup tasks
    console.log(`Left video room: ${theme}`);
  });

  socket.on("update_user_list", function (data) {
    console.log("Entrei")
    var onlineUsersList = document.getElementById("online-users");
    var offlineUsersList = document.getElementById('offline-users');
    var ocupadoUsersList = document.getElementById('ocupado-users');
    
    onlineUsersList.innerHTML = "";
    data.online_users.forEach(function (user) {
      var li = document.createElement("li");
      if(data.chat_users.includes(user)){
        li.appendChild(document.createTextNode(`${user} - Texto`));  // Corrigido aqui
      } else if(data.video_users.includes(user)){
        li.appendChild(document.createTextNode(`${user} - Vídeo`));  // Corrigido aqui
      } else {
        li.appendChild(document.createTextNode(`${user} - Texto e vídeo`));  // Corrigido aqui
      }
      onlineUsersList.appendChild(li);  // Corrigido aqui
    });

    offlineUsersList.innerHTML = "";

    data.offline_users.forEach(function (user) {
      var li = document.createElement("li"); 
      if(data.chat_users.includes(user)){
        li.appendChild(document.createTextNode(`${user} - Texto`));  // Corrigido aqui
      } else if(data.video_users.includes(user)){
        li.appendChild(document.createTextNode(`${user} - Vídeo`));  // Corrigido aqui
      } else {
        li.appendChild(document.createTextNode(`${user} - Texto e vídeo`));  // Corrigido aqui
      }

      offlineUsersList.appendChild(li);  // Corrigido aqui
    });

    ocupadoUsersList.innerHTML = "";
    data.ocupado_users.forEach(function (user) {
      var li = document.createElement("li");
      if(data.chat_users.includes(user)){
        li.appendChild(document.createTextNode(`${user} - Texto`));  // Corrigido aqui
      } else if(data.video_users.includes(user)){
        li.appendChild(document.createTextNode(`${user} - Vídeo`));  // Corrigido aqui
      } else {
        li.appendChild(document.createTextNode(`${user} - Texto e vídeo`));  // Corrigido aqui
      }
      ocupadoUsersList.appendChild(li);  // Corrigido aqui
    });
  });

