package shake;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.xml.ws.WebServiceRef;
import shake.DBclient.HashTable;
import shake.DBclient.HashTableWS_Service;


public class GetHashTBServlet extends HttpServlet {

    @WebServiceRef(wsdlLocation = "WEB-INF/wsdl/localhost_8080/HashTableWS/HashTableWS.wsdl")
    private HashTableWS_Service service;

   
    protected void processRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
            String action = request.getParameter("action");
            String IDstring = request.getParameter("id");
            int ID=0;
            if(IDstring!=null && !IDstring.equals("")){
                if(isNumeric(IDstring))
                    ID=Integer.parseInt(IDstring);
            }
            for(HashTable hashTable: getAllHashTB()){
                if(hashTable.getId()==ID){
                    hashTable = getHashTB(ID);
                    if("Wyswietl".equalsIgnoreCase(action)){
                        request.setAttribute("id", hashTable.getId());
                        request.setAttribute("tekst", hashTable.getTekst());
                        request.setAttribute("l_bitow", hashTable.getBity());
                        request.setAttribute("hash", hashTable.getShake128());
                    }else if(action.equalsIgnoreCase("Usun"))
                        removeHashTB(hashTable);                    
                    }
            }
            request.setAttribute("allHashes", getAllHashTB());
            request.getRequestDispatcher("allHashes.jsp").forward(request, response); 
    }
    public static boolean isNumeric(String str){
        for (char c : str.toCharArray())
            if (!Character.isDigit(c)) return false;
    return true;
}
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        processRequest(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        processRequest(request, response);
    }

 
    @Override
    public String getServletInfo() {
        return "Short description";
    }

    private HashTable getHashTB(int id) {
        shake.DBclient.HashTableWS port = service.getHashTableWSPort();
        return port.getHashTB(id);
    }

    private void removeHashTB(shake.DBclient.HashTable hashTB) {
        shake.DBclient.HashTableWS port = service.getHashTableWSPort();
        port.removeHashTB(hashTB);
    }


    private java.util.List<shake.DBclient.HashTable> getAllHashTB() {
        shake.DBclient.HashTableWS port = service.getHashTableWSPort();
        return port.getAllHashTB();
    }

}
