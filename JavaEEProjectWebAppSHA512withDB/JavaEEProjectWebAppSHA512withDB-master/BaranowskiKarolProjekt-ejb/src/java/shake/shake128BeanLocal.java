package shake;

import javax.ejb.Local;


@Local
public interface shake128BeanLocal {

    String getText();

    void setText(String text);

    int getBits();

    String getHash();

    void setHash(String hash);

    void setBits(int bits);
    
}
