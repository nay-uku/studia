package dbjpa;

import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;


@Stateless
public class HashTableFacade extends AbstractFacade<HashTable> implements HashTableFacadeLocal {

    @PersistenceContext(unitName = "BaranowskiKarolProjekt-DatabasePU")
    private EntityManager em;

    @Override
    protected EntityManager getEntityManager() {
        return em;
    }

    public HashTableFacade() {
        super(HashTable.class);
    }
    
}
