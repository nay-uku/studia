package shake;

import java.io.IOException;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.xml.ws.WebServiceRef;
import shake.DBclient.HashTable;
import shake.DBclient.HashTableWS_Service;


public class AddHashTBServlet extends HttpServlet {

    @WebServiceRef(wsdlLocation = "WEB-INF/wsdl/localhost_8080/HashTableWS/HashTableWS.wsdl")
    private HashTableWS_Service service;

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
        throws ServletException, IOException {
        String tekst = request.getParameter("tekst");
        String hash = request.getParameter("shake128");
        String bityStr = request.getParameter("l_bitow");
        
        if(tekst!=null && !tekst.equals("") && hash!=null && !hash.equals("") && bityStr!=null && !bityStr.equals("")){
            HashTable hashTable = new HashTable();
            hashTable.setShake128(hash);
            hashTable.setTekst(tekst);
            hashTable.setBity(Integer.parseInt(bityStr));
            addHashTB(hashTable); 
        }
        request.setAttribute("allHashes", getAllHashTB());
        request.getRequestDispatcher("allHashes.jsp").forward(request, response);
    }
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        
    }
    @Override
    public String getServletInfo() {
        return "Short description";
    }
    private void addHashTB(shake.DBclient.HashTable hashTB) {
        shake.DBclient.HashTableWS port = service.getHashTableWSPort();
        port.addHashTB(hashTB);
    }

    private java.util.List<shake.DBclient.HashTable> getAllHashTB() {
        // Note that the injected javax.xml.ws.Service reference as well as port objects are not thread safe.
        // If the calling of port operations may lead to race condition some synchronization is required.
        shake.DBclient.HashTableWS port = service.getHashTableWSPort();
        return port.getAllHashTB();
    }

}
