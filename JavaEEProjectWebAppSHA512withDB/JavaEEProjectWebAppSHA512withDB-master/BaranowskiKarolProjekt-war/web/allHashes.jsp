<%@page contentType="text/html" pageEncoding="UTF-8"%>
<%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
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
               
                   Tekst do wyliczenia funkcji skrótu: <input type="text" name="tekst" style="width:552px;" value="${tekst}" readonly></br>
                   Długość bitów wygenerowanej funkcji skrótu: <input type="text" name="l_bitow" style="width:457px;" value="${l_bitow}" readonly></br>
                   Wygenerowana funkcja skrótu: <input type="text" name="hash" style="width:575px;" readonly value="${hash}"></br>
            
                   <button><a href="<%="AddHashTBServlet?shake128="+request.getParameter("hash")+"&l_bitow="+request.getParameter("l_bitow")+"&tekst="+request.getParameter("tekst")%>">Dodaj</a></button>
                   <form action="GetHashTBServlet">
                    Podaj id w bazie: <input type="text" name="id" style="width:30px;" value="${id}" ></br>
                    <input name="action" id="sub" type="submit" value="Wyswietl">
                    <input name="action" id="sub" type="submit" value="Usun">
                   </form>
                </br>
                <button onclick="location.href='index.jsp'" type="button">Generuj nowy skrot</button></br></br>
                <h3>Baza funkcji skrótów:</h3>
                <table border="1">
                    <th>Id</th>
                    <th>Tekst</th>
                    <th>Shake128</th>
                    <th>Bity</th>
                    <c:forEach items="${allHashes}" var="line">
                        <tr>
                            <td>${line.id}</td>
                            <td>${line.tekst}</td>
                            <td>${line.shake128}</td>
                            <td>${line.bity}</td>
                        </tr>
                    </c:forEach>
            </table>  
            </div>
            <div class="rectangle">
               2019 &copy; Karol Baranowski. TJEE Projekt indywidualny. 
            </div>
         </div>
      </div>
   </body>
</html>
