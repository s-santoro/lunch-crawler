package ntb.iks.bolts;

import static com.digitalpebble.stormcrawler.Constants.StatusStreamName;

import java.util.Iterator;
import java.util.Map;

import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;

import com.digitalpebble.stormcrawler.Metadata;
import com.digitalpebble.stormcrawler.indexing.AbstractIndexerBolt;
import com.digitalpebble.stormcrawler.persistence.Status;
import java.io.*;
import java.nio.charset.Charset;


/**
 * Indexer which generates json-files with keys: "URL" and "Content"
 * for each found Website.
 */
@SuppressWarnings("serial")
public class OutputFileWriter extends AbstractIndexerBolt {
    OutputCollector _collector;

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
        // Create File
        String filenameURL = url.replaceAll("[^a-zA-Z0-9\\-]", "_");
        String filename = "/topology/Output/" + filenameURL + ".json";
        File file = new File(filename);
        file.getParentFile().mkdirs();
        try {
            file.createNewFile();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Write File
        PrintWriter out = null;
        try {
            out = new PrintWriter(new BufferedWriter(new FileWriter(filename, true)));
            out.println("{");
            out.println("\"url\": \""+ url +"\",");
            out.println("\"meta\": \""+ metadata +"\",");
            out.println("\"text: \""+text+ "\"");
            //out.println("\"content: \""+content+ "\"");
            out.println("}");
        }catch (IOException e) {
            System.err.println(e);
        }finally{
            if(out != null){
                out.close();
            }
        }
        //
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