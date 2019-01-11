package ntb.iks.bolts;

import static com.digitalpebble.stormcrawler.Constants.StatusStreamName;

import java.nio.charset.Charset;
import java.util.Iterator;
import java.util.Map;

import com.digitalpebble.stormcrawler.indexing.AbstractIndexerBolt;
import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;

import org.slf4j.LoggerFactory;
import com.digitalpebble.stormcrawler.Metadata;
import com.digitalpebble.stormcrawler.persistence.Status;

/**
 * Data collector which generates fields for indexing, prints them to the standard
 * output and emits them to next bolt for database-indexing.
 * Useful for debugging.
 */

//TODO: set code credit

@SuppressWarnings("serial")
public class DataCollectorBolt extends AbstractIndexerBolt
{
	OutputCollector _collector;
	private static final org.slf4j.Logger LOG = LoggerFactory
			.getLogger(DataCollectorBolt.class);

	@SuppressWarnings("rawtypes")
	@Override
	public void prepare(Map conf, TopologyContext context,
			OutputCollector collector) {
		super.prepare(conf, context, collector);
		_collector = collector;
	}

	@Override
	public void execute(Tuple tuple) {

		// TODO: decide if robots-meta-tags should be acknowledged
//		// should this document be kept?
//		boolean keep = filterDocument(metadata);
//		if (!keep) {
//			// treat it as successfully processed even if
//			// we do not index it
//			_collector.emit(StatusStreamName, tuple, new Values(url, metadata,
//					Status.FETCHED));
//			_collector.ack(tuple);
//			return;
//		}

		// print url to console
		String url = tuple.getStringByField("url");
		System.out.println();
		System.out.println();
		System.out.println("url:" + "\t" + url);
		// print metadata to console
		// which metadata to display?
		Metadata metadata = (Metadata) tuple.getValueByField("metadata");
		Map<String, String[]> keyVals = filterMetadata(metadata);
		Iterator<String> iterator = keyVals.keySet().iterator();
		String meta = "metadata:" + "\t";
		while (iterator.hasNext()) {
			String fieldName = iterator.next();
			String[] values = keyVals.get(fieldName);
			for (String value : values) {
				meta = meta + value + "\n";
			}
		}
		System.out.println();
		System.out.println();
		System.out.println(meta);
		// print content to console
		byte[] binary = tuple.getBinaryByField("content");
		String content = new String(binary, Charset.defaultCharset());
		System.out.println();
		System.out.println();
		System.out.println("content:" + "\t" + content);
		// print text to console
		String text = tuple.getStringByField("text");
		System.out.println();
		System.out.println();
		System.out.println("text:" + "\t" + text);


		// emit tuple for indexing
		// tuple: [url, metadata content, text]
		_collector.emit(StatusStreamName, tuple,
				new Values(url, meta, content, text));
		_collector.ack(tuple);
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declareStream(
				com.digitalpebble.stormcrawler.Constants.StatusStreamName,
				new Fields("url", "metadata", "content", "text"));
	}

	private String trimValue(String value) {
		if (value.length() > 100)
			return value.length() + " chars long, not printed on console";
		return value;
	}

}
