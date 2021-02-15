package dbjpa;

import java.io.Serializable;
import javax.persistence.Basic;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.NamedQueries;
import javax.persistence.NamedQuery;
import javax.persistence.Table;
import javax.validation.constraints.Size;
import javax.xml.bind.annotation.XmlRootElement;


@Entity
@Table(name = "HashTable")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "HashTable.findAll", query = "SELECT h FROM HashTable h")
    , @NamedQuery(name = "HashTable.findById", query = "SELECT h FROM HashTable h WHERE h.id = :id")
    , @NamedQuery(name = "HashTable.findByTekst", query = "SELECT h FROM HashTable h WHERE h.tekst = :tekst")
    , @NamedQuery(name = "HashTable.findByShake128", query = "SELECT h FROM HashTable h WHERE h.shake128 = :shake128")
    , @NamedQuery(name = "HashTable.findByBity", query = "SELECT h FROM HashTable h WHERE h.bity = :bity")})
public class HashTable implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "Id")
    private Integer id;
    @Size(max = 300)
    @Column(name = "Tekst")
    private String tekst;
    @Size(max = 300)
    @Column(name = "Shake128")
    private String shake128;
    @Column(name = "Bity")
    private Integer bity;

    public HashTable() {
    }

    public HashTable(Integer id) {
        this.id = id;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getTekst() {
        return tekst;
    }

    public void setTekst(String tekst) {
        this.tekst = tekst;
    }

    public String getShake128() {
        return shake128;
    }

    public void setShake128(String shake128) {
        this.shake128 = shake128;
    }

    public Integer getBity() {
        return bity;
    }

    public void setBity(Integer bity) {
        this.bity = bity;
    }

    @Override
    public int hashCode() {
        int hash = 0;
        hash += (id != null ? id.hashCode() : 0);
        return hash;
    }

    @Override
    public boolean equals(Object object) {
       
        if (!(object instanceof HashTable)) {
            return false;
        }
        HashTable other = (HashTable) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "dbjpa.HashTable[ id=" + id + " ]";
    }
    
}
