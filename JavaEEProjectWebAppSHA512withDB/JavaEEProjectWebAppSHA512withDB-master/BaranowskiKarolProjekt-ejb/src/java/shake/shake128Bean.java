package shake;

import javax.ejb.Stateless;


@Stateless
public class shake128Bean implements shake128BeanLocal {

    private String text;
    private String hash;
    private int bits;

    @Override
    public String getText() {
        return this.text;
    }

    @Override
    public void setText(String text) {
        this.text=text;
    }

    @Override
    public int getBits() {
        return this.bits;
    }

    @Override
    public String getHash() {
        return this.hash;
    }

    @Override
    public void setHash(String hash) {
        this.hash=hash;
    }

    @Override
    public void setBits(int bits) {
        this.bits=bits;
    }
    
    
    
    
}
