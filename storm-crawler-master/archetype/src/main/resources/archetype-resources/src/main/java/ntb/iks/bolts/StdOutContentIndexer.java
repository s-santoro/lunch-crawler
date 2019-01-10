package ntb.iks.bolts;

import static com.digitalpebble.stormcrawler.Constants.StatusStreamName;

import java.nio.charset.Charset;
import java.util.Iterator;
import java.util.Map;

import com.digitalpebble.stormcrawler.indexing.AbstractIndexerBolt;
import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;

import org.slf4j.LoggerFactory;
import com.digitalpebble.stormcrawler.Metadata;
import com.digitalpebble.stormcrawler.persistence.Status;

/**
 * Indexer which generates fields for indexing and sends them to the standard
 * output. Useful for debugging and as an illustration of what
 * AbstractIndexerBolt provides.
 */
@SuppressWarnings("serial")
public class StdOutContentIndexer extends AbstractIndexerBolt
{
	OutputCollector _collector;
	private static final org.slf4j.Logger LOG = LoggerFactory
			.getLogger(StdOutContentIndexer.class);

	@SuppressWarnings("rawtypes")
	@Override
	public void prepare(Map conf, TopologyContext context,
			OutputCollector collector) {
		super.prepare(conf, context, collector);
		_collector = collector;
	}

	@Override
	public void execute(Tuple tuple) {
		String url = tuple.getStringByField("url");

		// Distinguish the value used for indexing
		// from the one used for the status
		String normalisedurl = valueForURL(tuple);

		Metadata metadata = (Metadata) tuple.getValueByField("metadata");

		byte[] binary = tuple.getBinaryByField("content");
		String content = new String(binary, Charset.defaultCharset());
		String text1 = tuple.getStringByField("text");

		System.out.println();
		LOG.info("------------------------------------------------------------------------------------");
		LOG.info("Content: {}", content);
		LOG.info("------------------------------------------------------------------------------------");
		System.out.println();
		LOG.info("------------------------------------------------------------------------------------");
		LOG.info("Text: {}", text1);
		LOG.info("------------------------------------------------------------------------------------");
		System.out.println();

		// should this document be kept?
		boolean keep = filterDocument(metadata);
		if (!keep) {
			// treat it as successfully processed even if
			// we do not index it
			_collector.emit(StatusStreamName, tuple, new Values(url, metadata,
					Status.FETCHED));
			_collector.ack(tuple);
			return;
		}

		// display text of the document?
		if (fieldNameForText() != null) {
			String text = tuple.getStringByField("text");
			System.out.println(fieldNameForText() + "\t" + trimValue(text));
		}

		if (fieldNameForURL() != null) {
			System.out.println(fieldNameForURL() + "\t"
					+ trimValue(normalisedurl));
		}

		// which metadata to display?
		Map<String, String[]> keyVals = filterMetadata(metadata);

		Iterator<String> iterator = keyVals.keySet().iterator();
		while (iterator.hasNext()) {
			String fieldName = iterator.next();
			String[] values = keyVals.get(fieldName);
			for (String value : values) {
				System.out.println(fieldName + "\t" + trimValue(value));
			}
		}

		_collector.emit(StatusStreamName, tuple, new Values(url, metadata,
				Status.FETCHED));
		_collector.ack(tuple);
	}

	private String trimValue(String value) {
		if (value.length() > 100)
			return value.length() + " chars";
		return value;
	}

}
