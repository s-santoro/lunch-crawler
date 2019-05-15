package ntb.iks.bolts;

import static com.digitalpebble.stormcrawler.Constants.StatusStreamName;

import java.util.Iterator;
import java.util.Map;

import org.apache.storm.shade.org.apache.commons.lang.RandomStringUtils;
import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;
import org.json.simple.JSONObject;

import com.digitalpebble.stormcrawler.Metadata;
import com.digitalpebble.stormcrawler.indexing.AbstractIndexerBolt;
import com.digitalpebble.stormcrawler.persistence.Status;
import java.io.*;
import java.nio.charset.Charset;


// LANGUAGE DETECTION
//import java.io.IOException;
//import org.apache.tika.language.*;
//import org.apache.tika.language.detect.LanguageDetector;

import java.util.List;
import static java.util.Arrays.asList;

import com.github.pemistahl.lingua.api.LanguageDetectorBuilder;
import com.github.pemistahl.lingua.api.LanguageDetector;
import com.github.pemistahl.lingua.api.Language;
//

/**
 * Indexer which generates json-files with keys: "URL" and "Content"
 * for each found Website.
 */
@SuppressWarnings("serial")
public class SkinnyFileWriter extends AbstractIndexerBolt {
    OutputCollector _collector;

    @SuppressWarnings("rawtypes")
    @Override
    public void prepare(Map conf, TopologyContext context,
                        OutputCollector collector) {
        super.prepare(conf, context, collector);
        _collector = collector;
    }

    @SuppressWarnings("deprecation")
	@Override
    public void execute(Tuple tuple) {
        String url = tuple.getStringByField("url");
        String text = tuple.getStringByField("text");
        // Distinguish the value used for indexing
        // from the one used for the status
        String normalisedurl = valueForURL(tuple);

        Metadata metadata = (Metadata) tuple.getValueByField("metadata");

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

        //
        //
        // BA-CODE: Create Output-JSON-Files  and write them
        byte[] binary = tuple.getBinaryByField("content");
        String content = new String(binary, Charset.defaultCharset());
        String filenameURL = url.replaceAll("[^a-zA-Z0-9\\-]", "");
    	filenameURL = filenameURL.replaceAll("https", "");
    	filenameURL = filenameURL.replaceAll("http", "");
    	filenameURL = filenameURL.replaceAll("www", "");
    	if(filenameURL.length()>150) {
    		filenameURL = filenameURL.substring(0, 20)+"_"+RandomStringUtils.randomAlphanumeric(4);
    	}
        String filename = "/topology/Output/" + filenameURL + ".json";
        // Create JSON     
        JSONObject json = new JSONObject();
        json.put("date", metadata.getFirstValue("date"));
        json.put("encoding", metadata.getFirstValue("parse.Content-Encoding"));
        json.put("title", metadata.getFirstValue("parse.title"));
        json.put("url", url);   
        json.put("text", text);
        json.put("content", content);
        //
        // Write JSON to File
        FileWriter file = null;
        try {
			file = new FileWriter(filename);
			file.write(json.toJSONString());
		} catch (IOException e) {
			e.printStackTrace();
		}finally {
			try {
				file.flush();
				file.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
        
        //
        //
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