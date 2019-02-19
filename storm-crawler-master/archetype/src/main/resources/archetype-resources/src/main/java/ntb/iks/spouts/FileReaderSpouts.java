package ntb.iks.spouts;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

public class FileReaderSpouts
{
	ArrayList<String> urlList;
	File seedFile;

	public FileReaderSpouts(String seedPath) {
		seedFile = new File(seedPath);
		urlList = new ArrayList<String>();
	}

	public String[] getUrls()
	{
		try {

		BufferedReader br = new BufferedReader(new java.io.FileReader(seedFile));
		String url;
		while((url = br.readLine()) != null) {
			System.out.println(url);
			urlList.add(url);
		}
		br.close();
		}
		catch (IOException e) {
			e.printStackTrace();
		}
		return (String[])urlList.toArray(new String[0]);
	}


}
