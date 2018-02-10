package team.qep.crawler.util;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Date;
import java.util.HashSet;
import java.util.Set;

//字符串操作
public class StringManipulation {
	//一维list转二维数组(只有一列)
	public static String[][] toTwoDimensionalArrays(ArrayList<String> strlist){
		String[][] str = new String[strlist.size()][1];
		for(int i = 0 ; i < strlist.size() ; i++) {
			str[i][0] = strlist.get(i);
		}
		return str;
	}
	//一维字符数组转指定二维数组      参数--待转的一维字符数组  转换的维度
	public static String[][] toTwoDimensionalArrays(String[] string,int dimension){
		String[][] twoDimensional = new String[string.length/dimension][dimension];
		for(int i=1 ; i < string.length ; i++) {
			twoDimensional[(i-1)/dimension][(i-1)%dimension] = string[i];
		}
		return twoDimensional;
	}
		
	//二位数组转一维数组(只取第一列)
	public static String[] toOneDimensionalArrays(String[][] string){
		String[] str = new String[string.length];
		for(int i = 0 ; i < string.length ; i++) {
			str[i] = string[i][0];
		}
		return str;
	}
	//二维数组转二维数组(只取其中几列)
	public static String[][] twoToTwo(String[][] string,int cloum){
		String[][] str = new String[string.length][1];
		for(int i = 0 ; i < string.length ; i++) {
			str[i][0] = string[i][cloum];
		}
		return str;
	}
	//二维数组排序(按cloum[0],cloum[1]依次排序)
	public static void sortByColumn(String[][] str,int cloum[]){
		Arrays.sort(str,new Comparator<String[]>() {
			public int compare(String[] o1,String[] o2) {
				try {
					DateFormat df = new SimpleDateFormat("HH:mm:ss");
					
					for(int i=0 ; i<cloum.length ; i++){
						Date dt1 = df.parse(o1[cloum[i]]);
						Date dt2 = df.parse(o2[cloum[i]]);
						if(dt1.getTime()>dt2.getTime()){
							return 1;
						}else if(dt1.getTime()<dt2.getTime()){
							return -1;
						}
					}
				} catch (ParseException e) {
					e.printStackTrace();
				}
				return 0;
			}
		});
	}
	
	//一维数组去重
	public static String[] oneDuplicateRemoval(String[] string){
		Set<String> set = new HashSet<String>(Arrays.asList(string));
		return set.toArray(new String[set.size()]);
	}
	//检测字符串是否出现过
	public static boolean duplicateDetection(String[][] string,String str){
		for(int i = 0 ; i < string.length ; i++) {
			if(str.equals(string[i][1])){
				return true;
			}
		}
		return false;
	}
	
	public static String[][] mergeResources(String[][] str){
        ArrayList<String[]> list = new ArrayList<String[]>();
        for (int i = 0; i < str.length; i++) {
                list.add(str[i]);
        }
        for (int i = 0; i < list.size(); i++) {
            for (int j = i+1; j < list.size(); j++) {
            	if(list.get(i)[0].equals(list.get(j)[0]) && list.get(i)[1].equals(list.get(j)[1])){
            		list.get(i)[3] = new String(list.get(i)[3]+","+list.get(j)[3]);
            		list.remove(j);
            		j--;
            	}
            }
        }
        String[][] string=new String[list.size()][];
        for (int i = 0; i < list.size(); i++) {
        	string[i]=list.get(i);
        }
        return string;
	}
	public static void main(String[] args){
		String[][] a =	new String[][]{ { "0", "","1" }, { "0", "","2" }, 
				{ "1", "","2" },{ "1", "","3" },{ "1", "","4" }, { "2", "gdh","4" } };
		a=mergeResources( a);
		for (int i = 0; i < a.length; i++) {
		   	System.out.println("结果s"+Arrays.toString(a[i]));
		}
	}
}

