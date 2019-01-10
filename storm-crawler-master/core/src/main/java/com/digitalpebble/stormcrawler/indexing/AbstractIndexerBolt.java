/**
 * Licensed to DigitalPebble Ltd under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * DigitalPebble licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.digitalpebble.stormcrawler.indexing;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.commons.lang.ArrayUtils;
import org.apache.commons.lang.StringUtils;
import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichBolt;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Tuple;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.digitalpebble.stormcrawler.Metadata;
import com.digitalpebble.stormcrawler.util.ConfUtils;
import com.digitalpebble.stormcrawler.util.RobotsTags;
import com.digitalpebble.stormcrawler.util.URLUtil;

/** Abstract class to simplify writing IndexerBolts **/
@SuppressWarnings("serial")
public abstract class AbstractIndexerBolt extends BaseRichBolt {

    private final Logger LOG = LoggerFactory.getLogger(getClass());

    /**
     * Mapping between metadata keys and field names for indexing Can be a list
     * of values separated by a = or a single string
     **/
    public static final String metadata2fieldParamName = "indexer.md.mapping";

    /**
     * list of metadata key + values to be used as a filter. A document will be
     * indexed only if it has such a md. Can be null in which case we don't
     * filter at all.
     **/
    public static final String metadataFilterParamName = "indexer.md.filter";

    /** Field name to use for storing the text of a document **/
    public static final String textFieldParamName = "indexer.text.fieldname";

    /** Trim length of text to index. Defaults to -1 to keep it intact **/
    public static final String textLengthParamName = "indexer.text.maxlength";

    /** Field name to use for storing the url of a document **/
    public static final String urlFieldParamName = "indexer.url.fieldname";

    /** Field name to use for reading the canonical property of the metadata */
    public static final String canonicalMetadataParamName = "indexer.canonical.name";

    private String[] filterKeyValue = null;

    private Map<String, String> metadata2field = new HashMap<>();

    private String fieldNameForText = null;

    private int maxLengthText = -1;

    private String fieldNameForURL = null;

    private String canonicalMetadataName = null;

    @SuppressWarnings({ "rawtypes", "unchecked" })
    @Override
    public void prepare(Map conf, TopologyContext context,
            OutputCollector collector) {

        String mdF = ConfUtils.getString(conf, metadataFilterParamName);
        if (StringUtils.isNotBlank(mdF)) {
            // split it in key value
            int equals = mdF.indexOf('=');
            if (equals != -1) {
                String key = mdF.substring(0, equals);
                String value = mdF.substring(equals + 1);
                filterKeyValue = new String[] { key.trim(), value.trim() };
            } else {
                LOG.error("Can't split into key value : {}", mdF);
            }
        }

        fieldNameForText = ConfUtils.getString(conf, textFieldParamName);

        maxLengthText = ConfUtils.getInt(conf, textLengthParamName, -1);

        fieldNameForURL = ConfUtils.getString(conf, urlFieldParamName);

        canonicalMetadataName = ConfUtils.getString(conf,
                canonicalMetadataParamName);

        for (String mapping : ConfUtils.loadListFromConf(
                metadata2fieldParamName, conf)) {
            int equals = mapping.indexOf('=');
            if (equals != -1) {
                String key = mapping.substring(0, equals);
                String value = mapping.substring(equals + 1);
                metadata2field.put(key.trim(), value.trim());
            } else {
                LOG.error("Can't split into key value : {}", mapping);
            }
        }
    }

    /**
     * Determine whether a document should be indexed based on the presence of a
     * given key/value or the RobotsTags.ROBOTS_NO_INDEX directive.
     * 
     * @return true if the document should be kept.
     **/
    protected boolean filterDocument(Metadata meta) {
        String noindexVal = meta.getFirstValue(RobotsTags.ROBOTS_NO_INDEX);
        if ("true".equalsIgnoreCase(noindexVal))
            return false;

        if (filterKeyValue == null)
            return true;
        String[] values = meta.getValues(filterKeyValue[0]);
        // key not found
        if (values == null)
            return false;
        return ArrayUtils.contains(values, filterKeyValue[1]);
    }

    /** Returns a mapping field name / values for the metadata to index **/
    protected Map<String, String[]> filterMetadata(Metadata meta) {

        Pattern indexValuePattern = Pattern.compile("\\[(\\d+)\\]");

        Map<String, String[]> fieldVals = new HashMap<>();
        Iterator<Entry<String, String>> iter = metadata2field.entrySet()
                .iterator();
        while (iter.hasNext()) {
            Entry<String, String> entry = iter.next();
            // check whether we want a specific value or all of them?
            int index = -1;
            String key = entry.getKey();
            Matcher match = indexValuePattern.matcher(key);
            if (match.find()) {
                index = Integer.parseInt(match.group(1));
                key = key.substring(0, match.start());
            }
            String[] values = meta.getValues(key);
            // not found
            if (values == null || values.length == 0)
                continue;
            // want a value index that it outside the range given
            if (index >= values.length)
                continue;
            // store all values available
            if (index == -1)
                fieldVals.put(entry.getValue(), values);
            // or only the one we want
            else
                fieldVals.put(entry.getValue(), new String[] { values[index] });
        }

        return fieldVals;
    }

    /**
     * Returns the value to be used as the URL for indexing purposes, if present
     * the canonical value is used instead
     */
    protected String valueForURL(Tuple tuple) {

        String url = tuple.getStringByField("url");
        Metadata metadata = (Metadata) tuple.getValueByField("metadata");

        // functionality deactivated
        if (StringUtils.isBlank(canonicalMetadataParamName)) {
            return url;
        }

        String canonicalValue = metadata.getFirstValue(canonicalMetadataName);

        // no value found?
        if (StringUtils.isBlank(canonicalValue)) {
            return url;
        }

        try {
            URL sURL = new URL(url);
            URL canonical = URLUtil.resolveURL(sURL, canonicalValue);

            // check is the same host
            if (sURL.getHost().equals(canonical.getHost())) {
                return canonical.toExternalForm();
            } else {
                LOG.info(
                        "Canonical URL references a different host, ignoring in {} ",
                        url);
            }
        } catch (MalformedURLException e) {
            LOG.error("Malformed canonical URL {} was found in {} ",
                    canonicalValue, url);
        }

        return url;
    }

    /**
     * Returns the field name to use for the text or null if the text must not
     * be indexed
     **/
    protected String fieldNameForText() {
        return fieldNameForText;
    }

    /**
     * Returns a trimmed string or the original one if it is below the threshold
     * set in the configuration.
     **/
    protected String trimText(String text) {
        if (maxLengthText == -1)
            return text;
        if (text == null)
            return text;
        if (text.length() <= maxLengthText)
            return text;
        return text.substring(0, maxLengthText);
    }

    /**
     * Returns the field name to use for the URL or null if the URL must not be
     * indexed
     **/
    protected String fieldNameForURL() {
        return fieldNameForURL;
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        declarer.declareStream(
                com.digitalpebble.stormcrawler.Constants.StatusStreamName,
                new Fields("url", "metadata", "status"));
    }
}
