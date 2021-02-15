package shake;

import java.io.IOException;

import javax.ejb.EJB;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.xml.ws.WebServiceRef;
import shake.DBclient.HashTableWS_Service;



@WebServlet(name = "Shake128Servlet", urlPatterns = {"/Shake128Servlet"})
public class Shake128Servlet extends HttpServlet {

    @WebServiceRef(wsdlLocation = "WEB-INF/wsdl/localhost_8080/HashTableWS/HashTableWS.wsdl")
    private HashTableWS_Service service_1;

    @WebServiceRef(wsdlLocation = "http://localhost:8080/shake128WS/shake128WS?WSDL")
    
    private Shake128WS_Service service;
    
    String tekst;
    String hash;
    int bits;
    int id;

    protected void processRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
       
            tekst=request.getParameter("tekst");
            hash=request.getParameter("hash");
            bits=Integer.parseInt(request.getParameter("l_bitow")); 
            setText(tekst);
            setHash(hash);
            setBits(bits);
            
        request.setAttribute("tekst", getText());
        request.setAttribute("l_bitow", getBits());
        request.setAttribute("hash", getHash());
        request.setAttribute("allHashes", getAllHashTB());
        request.getRequestDispatcher("allHashes.jsp").forward(request, response);
    }

    // <editor-fold defaultstate="collapsed" desc="HttpServlet methods. Click on the + sign on the left to edit the code.">
    /**
     * Handles the HTTP <code>GET</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        processRequest(request, response);
    }

    /**
     * Handles the HTTP <code>POST</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        processRequest(request, response);
    }

    /**
     * Returns a short description of the servlet.
     *
     * @return a String containing servlet description
     */
    @Override
    public String getServletInfo() {
        return "Short description";
    }// </editor-fold>

    private void setText(java.lang.String text) {
        shake.Shake128WS port = service.getShake128WSPort();
        port.setText(text);
    }

    private String getText() {
        shake.Shake128WS port = service.getShake128WSPort();
        return port.getText();
    }

    private String getHash() {
        shake.Shake128WS port = service.getShake128WSPort();
        return port.getHash();
    }

    private int getBits() {
        shake.Shake128WS port = service.getShake128WSPort();
        return port.getBits();
    }

    private void setBits(int bits) {
        shake.Shake128WS port = service.getShake128WSPort();
        port.setBits(bits);
    }

    private void setHash(java.lang.String hash) {
        shake.Shake128WS port = service.getShake128WSPort();
        port.setHash(hash);
    }

    private java.util.List<shake.DBclient.HashTable> getAllHashTB() {
        // Note that the injected javax.xml.ws.Service reference as well as port objects are not thread safe.
        // If the calling of port operations may lead to race condition some synchronization is required.
        shake.DBclient.HashTableWS port = service_1.getHashTableWSPort();
        return port.getAllHashTB();
    }
  

}
