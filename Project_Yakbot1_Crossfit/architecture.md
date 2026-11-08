# Architecture

1. The project will be an application of CrossFit Box using javascript, HTML and CSS to make format and to put it presentable.

2. Into the application, there are two screens, one for the computer (teacher) and the second one to the mobile phone (student). 

3. The user of the computer (teacher) would create the execise and the mobile phone (practitioner) will see the time running when the teacher clicks the start button.

4. The teacher can choose For Time (count up to a time cap, with an option to finish early), AMRAP (count down from a time cap), or EMOM. EMOM preserves the automatic or manual exercise progression.

5. To share the teacher's workout with a phone on the same Wi-Fi, run `python server.py` from the project folder and open the computer's Wi-Fi address on both devices. The server holds the current workout in memory and the student screen polls it for updates. Keep the server running during the session; it is intended for a trusted local network.

6. For Time and AMRAP use a configurable 1-to-120-minute cap and display the selected routine on the practitioner screen. For Time ends at its cap or when the teacher finishes it; AMRAP ends when its countdown reaches zero.