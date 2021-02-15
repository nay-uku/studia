package dbjpa.ws;

import dbjpa.HashTable;
import dbjpa.HashTableFacadeLocal;
import java.util.List;
import javax.ejb.EJB;
import javax.jws.WebService;
import javax.jws.WebMethod;
import javax.jws.WebParam;
import javax.ejb.Stateless;


@WebService(serviceName = "HashTableWS")
@Stateless()
public class HashTableWS {

    @EJB
    private HashTableFacadeLocal hashTableFacade;
    
    @WebMethod(operationName = "addHashTB")
    public void addHashTB(@WebParam(name = "hashTB") HashTable hashTB){
        hashTableFacade.create(hashTB);
    }
    
    @WebMethod(operationName = "removeHashTB")
    public void removeHashTB(@WebParam(name = "hashTB") HashTable hashTB){
        hashTableFacade.remove(hashTB);
    }
    
    @WebMethod(operationName = "getHashTB")
    public HashTable getHashTB(@WebParam(name = "id") int id){
        return hashTableFacade.find(id);
    }
    
    @WebMethod(operationName = "getAllHashTB")
    public List<HashTable> getAllHashTB(){
        return hashTableFacade.findAll();
    }
}
