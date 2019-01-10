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

package com.digitalpebble.stormcrawler.indexer;

import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.tuple.Tuple;

import com.digitalpebble.stormcrawler.Metadata;
import com.digitalpebble.stormcrawler.indexing.AbstractIndexerBolt;

public class DummyIndexer extends AbstractIndexerBolt {
    OutputCollector _collector;
    Map<String, String> fields;

    @SuppressWarnings("rawtypes")
    @Override
    public void prepare(Map conf, TopologyContext context,
            OutputCollector collector) {
        super.prepare(conf, context, collector);
        _collector = collector;
        fields = new HashMap<>();
    }

    @Override
    public void execute(Tuple tuple) {
        String url = tuple.getStringByField("url");
        // Distinguish the value used for indexing
        // from the one used for the status
        String normalisedurl = valueForURL(tuple);
        Metadata metadata = (Metadata) tuple.getValueByField("metadata");
        String text = tuple.getStringByField("text");

        // tested by the TestOutputCollector
        boolean keep = filterDocument(metadata);
        if (!keep) {
            _collector.ack(tuple);
            return;
        }

        // display text of the document?
        if (fieldNameForText() != null) {
            fields.put(fieldNameForText(), trimText(text));
        }

        if (fieldNameForURL() != null) {
            fields.put(fieldNameForURL(), normalisedurl);
        }

        // which metadata to display?
        Map<String, String[]> keyVals = filterMetadata(metadata);

        Iterator<String> iterator = keyVals.keySet().iterator();
        while (iterator.hasNext()) {
            String fieldName = iterator.next();
            String[] values = keyVals.get(fieldName);
            for (String value : values) {
                fields.put(fieldName, value);
            }
        }

        _collector.ack(tuple);
    }

    private String trimValue(String value) {
        if (value.length() > 100)
            return value.length() + " chars";
        return value;
    }

    public Map<String, String> returnFields() {
        return fields;
    }
}
