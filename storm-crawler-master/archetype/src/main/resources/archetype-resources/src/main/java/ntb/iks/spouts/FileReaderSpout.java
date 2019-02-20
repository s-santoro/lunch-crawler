package ntb.iks.spouts;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

public class FileReaderSpout
{
	ArrayList<String> urlList;
	File seedFile;

	public FileReaderSpout(String seedPath) {
		seedFile = new File(seedPath);
		urlList = new ArrayList<String>();
	}

	public String[] getUrls()
	{
		// url needs to be in following format:
		// "http://www.valentinos-chur.ch/"
		String urlPrefix = "http://www.";
		String urlSuffix = "/";
		try {

		BufferedReader br = new BufferedReader(new java.io.FileReader(seedFile));
		String url;
		while((url = br.readLine()) != null) {
			urlList.add(urlPrefix+url+urlSuffix);
		}
		br.close();
		}
		catch (IOException e) {
			e.printStackTrace();
		}
		return (String[])urlList.toArray(new String[0]);
	}


}
