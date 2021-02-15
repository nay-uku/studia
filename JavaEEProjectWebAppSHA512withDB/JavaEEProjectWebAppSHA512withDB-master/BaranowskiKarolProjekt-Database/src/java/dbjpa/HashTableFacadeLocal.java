package dbjpa;

import java.util.List;
import javax.ejb.Local;


@Local
public interface HashTableFacadeLocal {

    void create(HashTable hashTable);

    void edit(HashTable hashTable);

    void remove(HashTable hashTable);

    HashTable find(Object id);

    List<HashTable> findAll();

    List<HashTable> findRange(int[] range);

    int count();
    
}
