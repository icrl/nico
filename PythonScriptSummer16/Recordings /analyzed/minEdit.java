public class minEdit
{
	
	/**
	 ** YIKES
	**/
	public void main(String[] args)
	{
		//figure out how to take in two .txt files
		//for loop, goes as many times as the number of lines in the file
			//parse through each file, feeding two corresponding lines from each .txt file into the minEditDistance method
			//save the output of each corresponding line to another file
		//calculate the total word error rate from the distance between each line
		//save that to the same file

		//wait but I could also just feed the entire .txt files in string form, if a new line counts as whitespace
	}

	private int minEditDistance(String expected, String interpreted)
	{
		//may want this to take in multiple lines, would "\\s+" allow new lines as well?
		String[] eArray = expected.split("\\s+");
		String[] iArray = interpreted.split("\\s+");
		int eLen = eArray.length;
		int iLen = iArray.length;

		//create a 2d array to hold the edit distance with 
		int[][] distance = new int[eLen + 1][iLen + 1];

		//for each row, set it from 0 to e length
		for(int i = 0; i <= eLen; i++)
		{
			distance[i][0] = i;
		}
		for(int j = 0; j <= iLen; j++)
		{
			distance[0][j] = j;
		}

		//go through and determine the distance between each word
		for(int i = 1; i <= eLen; i++)
		{
			for(int j = 1; j <= iLen; j++)
			{
				//if the two words are equal
				if(eArray[i-1].equals(iArray[j-1]))
				{
					//the distance is the same as the previous words
					distance[i][j] = distance[i-1][j-1];
				}
				else
				{
					//find the cost of substituting, inserting, and deleting
					int sub = distance[i-1][j-1] + 2;
					int ins = distance[i-1][j] + 1;
					int del = distance[i][j-1] + 1;

					//the distance is whichever is  smallest
					distance[i][j] = Math.min(Math.min(sub, ins), del);
				}
			}
		}
		//return the last value
		return distance[eLen][iLen];
	}

}
