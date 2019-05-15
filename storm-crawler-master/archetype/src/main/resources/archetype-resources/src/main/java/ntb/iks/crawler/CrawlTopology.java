package ntb.iks.crawler;

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

import com.digitalpebble.stormcrawler.*;
import com.digitalpebble.stormcrawler.bolt.FetcherBolt;
import com.digitalpebble.stormcrawler.bolt.JSoupParserBolt;
import com.digitalpebble.stormcrawler.bolt.SiteMapParserBolt;
import com.digitalpebble.stormcrawler.bolt.URLPartitionerBolt;
import com.digitalpebble.stormcrawler.bolt.FeedParserBolt;
import com.digitalpebble.stormcrawler.indexing.StdOutIndexer;
import com.digitalpebble.stormcrawler.persistence.MemoryStatusUpdater;
import com.digitalpebble.stormcrawler.persistence.StdOutStatusUpdater;
import com.digitalpebble.stormcrawler.spout.FileSpout;
import com.digitalpebble.stormcrawler.spout.MemorySpout;

import ntb.iks.bolts.CustomMemoryStatusUpdater;
import ntb.iks.bolts.OutputFileWriter;
import ntb.iks.bolts.SkinnyFileWriter;
import org.apache.storm.topology.TopologyBuilder;
import org.apache.storm.tuple.Fields;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Dummy topology to play with the spouts and bolts
 */
public class CrawlTopology extends ConfigurableTopology {

    public static void main(String[] args) throws Exception {
        ConfigurableTopology.start(new CrawlTopology(), args);
    }

    @Override
    protected int run(String[] args) {
    	
    	TopologyBuilder builder = new TopologyBuilder();
    	
        String seedPath = "/topology/";
        //FileReaderSpout fileReaderSpouts = new FileReaderSpout(seedPath);
        //String[] testURLs = fileReaderSpouts.getUrls();
        //LOG.info("-------- files loaded: ", testURLs);
        //String[] testURLs = new String[] { "http://www.limmatbruecke.ch", "http://www.limmathof.com", "http://www.limmat-restaurant.ch", "http://www.lincoln21.ch", "http://www.linde-baden.ch", "http://www.linde-basel.ch", "http://www.linde-belp.ch", "http://www.lindeberschis.ch", "http://www.linde-daiwil.ch", "http://www.lochergut.net", "http://www.littleitaly-sh.ch", "http://www.little-panda.ch", "http://www.lintakeaway.ch", "http://www.lindewurm.ch", "http://www.linde-uster.ch", "http://www.linden-pub.ch", "http://www.linde-embrach.ch", "http://www.linde-dettighofen.ch" };
        String[] testURLs = new String[] { "" };
        builder.setSpout("file", new FileSpout(seedPath, "seed.txt", false));

        builder.setSpout("spout", new MemorySpout(testURLs));

        builder.setBolt("partitioner", new URLPartitionerBolt())
                .shuffleGrouping("file")
                .shuffleGrouping("spout");

        builder.setBolt("fetch", new FetcherBolt())
                .fieldsGrouping("partitioner", new Fields("key"));

        builder.setBolt("sitemap", new SiteMapParserBolt())
                .localOrShuffleGrouping("fetch");

        builder.setBolt("feeds", new FeedParserBolt())
                .localOrShuffleGrouping("sitemap");

        builder.setBolt("parse", new JSoupParserBolt())
                .localOrShuffleGrouping("feeds");

        builder.setBolt("index", new OutputFileWriter())
                .localOrShuffleGrouping("parse");

        Fields furl = new Fields("url");

        // can also use MemoryStatusUpdater for simple recursive crawls
        // StdOutStatusUpdater
        builder.setBolt("status", new MemoryStatusUpdater())
                .fieldsGrouping("fetch", Constants.StatusStreamName, furl)
                .fieldsGrouping("sitemap", Constants.StatusStreamName, furl)
                .fieldsGrouping("feeds", Constants.StatusStreamName, furl)
                .fieldsGrouping("parse", Constants.StatusStreamName, furl)
                .fieldsGrouping("index", Constants.StatusStreamName, furl);

        return submit("crawl", conf, builder);
    }
}
