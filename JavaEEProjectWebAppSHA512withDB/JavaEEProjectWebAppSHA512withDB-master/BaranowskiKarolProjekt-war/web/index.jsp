<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang ="pl">
   <head>
      <meta charset="utf-8"/>
      <meta http-equiv="X-UA-Comapatible" content="IE=edge,chrome=1"/>
      <title>Shake-128</title>
      <link rel="stylesheet" href = "style.css" type = "text/css" />
      <link href="https://fonts.googleapis.com/css?family=Didact+Gothic|Josefin+Sans|Josefin+Slab:400,700i&amp;subset=latin-ext" rel="stylesheet">
      <script src="timer.js"></script>
      <script src="main.js"></script>
   </head>
   <body onload="odliczanie();">
      <div id="container">
         <div class="rectangle1">
            <div id="logo"><img src="pad.png" height="50px;" alt="">SHAKE-128</div>
            
            <div id="timer"></div>
            <div style="clear: both;"></div>
         </div>
         <div class="square">
            <div class="tile5">
               <h3>Podaj tekst do wyliczenia shake-128:</h3>
               <button onclick="displayResult();">Generuj</button>
               <form action="Shake128Servlet" method="POST" name="f">
                 
                   Podaj tekst do wyliczenia funkcji skrótu: <input type="text" name="tekst" style="width:500px;" ></br>
                   Podaj długość bitów wygenerowanej funkcji skrótu: <input type="text" name="l_bitow" style="width:403px;" ></br>
                   Wygenerowana funkcja skrótu: <input type="text" name="hash" style="width:572px;" readonly ></br> 
                   
                    <input name="sub" id="sub" type="submit" value="Przejdz do zarzadzania" style="visibility: hidden;">
               </form>
               <script>
                    function displayResult() {
                        if(parseInt(document.f.l_bitow.value,10)>256 || parseInt(document.f.l_bitow.value,10)<8 || document.f.tekst.value === ""|| document.f.tekst.value === null || document.f.l_bitow.value===""|| document.f.l_bitow.value===null||isNaN(document.f.l_bitow.value))
                            return
                        else{
                        document.f.hash.value = shake128(document.f.tekst.value, parseInt(document.f.l_bitow.value,10));
                        document.f.sub.style.visibility="visible";
                    }
                    }
                </script>
                </br>
            </div>
            <div class="rectangle">
               2019 &copy; Karol Baranowski. TJEE Projekt indywidualny. 
            </div>
         </div>
      </div>
   </body>
</html>
