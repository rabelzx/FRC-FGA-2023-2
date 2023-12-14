const socket = io.connect("http://localhost:5000");

function joinTheme() {
  // Obtenha o valor selecionado no seletor de tema
  const theme = document.getElementById("themeSelector").value;
  socket.emit("join", { theme: theme });
}

socket.on("theme_joined", (theme) => {
  navigator.mediaDevices
    .getUserMedia({ video: true, audio: true })
    .then((stream) => {
      const localVideo = document.getElementById("localVideo");
      localVideo.srcObject = stream;

      const peerConnection = new RTCPeerConnection();

      stream.getTracks().forEach((track) => peerConnection.addTrack(track, stream));

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
