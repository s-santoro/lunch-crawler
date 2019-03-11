package ntb.iks.bolts;
import java.util.Date;
import java.util.concurrent.atomic.AtomicInteger;

import com.digitalpebble.stormcrawler.Metadata;
import com.digitalpebble.stormcrawler.persistence.AbstractStatusUpdaterBolt;
import com.digitalpebble.stormcrawler.persistence.DefaultScheduler;
import com.digitalpebble.stormcrawler.persistence.Status;
import com.digitalpebble.stormcrawler.spout.MemorySpout;

/**
 * Use in combination with the MemorySpout for testing in local mode. There is
 * no guarantee that this will work in distributed mode as it expects the
 * MemorySpout to be in the same execution thread.
 **/
@SuppressWarnings("serial")
public class CustomMemoryStatusUpdater extends AbstractStatusUpdaterBolt {
	AtomicInteger count = new AtomicInteger();	
    @Override
    public void store(String url, Status status, Metadata metadata,
            Date nextFetch) throws Exception {
    		
        // by convention we do not refetch URLs with a next fetch date of EPOCH
        if (nextFetch.equals(DefaultScheduler.NEVER))
            return;
        if(count.getAndIncrement()<60) {
        	MemorySpout.add(url, metadata, nextFetch);
        }
        
    }


}