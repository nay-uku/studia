package shake;

import javax.ejb.EJB;
import javax.jws.WebService;
import javax.ejb.Stateless;
import javax.jws.Oneway;
import javax.jws.WebMethod;
import javax.jws.WebParam;


@WebService(serviceName = "shake128WS")
@Stateless()
public class shake128WS {

    @EJB
    private shake128BeanLocal ejbRef;// Add business logic below. (Right-click in editor and choose
    // "Insert Code > Add Web Service Operation")

    @WebMethod(operationName = "getText")
    public String getText() {
        return ejbRef.getText();
    }
    @WebMethod(operationName = "getHash")
    public String getHash() {
        return ejbRef.getHash();
    }
    @WebMethod(operationName = "getBits")
    public int getBits() {
        return ejbRef.getBits();
    }
    @WebMethod(operationName = "setText")
    @Oneway
    public void setText(@WebParam(name = "text") String text) {
        ejbRef.setText(text);
    }
    @WebMethod(operationName = "setHash")
    @Oneway
    public void setHash(@WebParam(name = "hash") String hash) {
        ejbRef.setHash(hash);
    }
    @WebMethod(operationName = "setBits")
    @Oneway
    public void setBits(@WebParam(name = "bits") int bits) {
        ejbRef.setBits(bits);
    }
    
    
}
