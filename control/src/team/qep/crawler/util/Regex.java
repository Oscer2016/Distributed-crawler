package team.qep.crawler.util;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

//正则匹配IP
public class Regex {
	public static String regIP ="^(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|[1-9])\\."
								+"(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)\\."
								+"(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)\\."
								+"(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)$";
	public static boolean RE_matching(String str,String model){
		Pattern pattern=Pattern.compile(model);
		Matcher matcher=pattern.matcher(str);
		return matcher.matches();
	}
}
