package ntb.iks.bolts;

import com.digitalpebble.stormcrawler.Metadata;
import com.digitalpebble.stormcrawler.persistence.AbstractStatusUpdaterBolt;
import com.digitalpebble.stormcrawler.persistence.Status;

import java.util.Date;

/**
 * Dummy status updater which dumps the content of the incoming tuples to the
 * standard output. Useful for debugging and as an illustration of what
 * AbstractStatusUpdaterBolt provides.
 */
@SuppressWarnings("serial")
public class DBIndexerBolt
{
//	@Override
//	public void store(String url, Status status, Metadata metadata, String content,
//			Date nextFetch) throws Exception {
//		System.out.println(url + "\t" + status + "\t" + nextFetch);
//		System.out.println(metadata.toString("\t") + "\t" + content);
//	}
}