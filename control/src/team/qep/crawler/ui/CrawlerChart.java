package team.qep.crawler.ui;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartUtilities;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.CategoryAxis;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.labels.StandardCategoryItemLabelGenerator;
import org.jfree.chart.labels.StandardPieSectionLabelGenerator;
import org.jfree.chart.plot.CategoryPlot;
import org.jfree.chart.plot.PiePlot;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.renderer.category.LineAndShapeRenderer;
import org.jfree.data.category.DefaultCategoryDataset;
import org.jfree.data.general.DefaultPieDataset;

import team.qep.crawler.server.Data;

public class CrawlerChart {
	//得到折线图
	public static JFreeChart getLineChart() {
		// JFreeChart对象 参数：标题，目录轴显示标签，数据轴显示标签，数据集，是否显示图例，是否生成工具，是否生成URL连接
		JFreeChart jfreechart = ChartFactory.createLineChart("Task Schedule", "", "", null,
				PlotOrientation.VERTICAL, true, true, false);

		// jfreechart.setBorderVisible(true);// 边框可见
		jfreechart.getLegend().setItemFont(new Font("微软雅黑", 1, 15));// 图例字体

		CategoryPlot categoryplot = (CategoryPlot) jfreechart.getPlot(); // 获取折线图plot对象
		categoryplot.setDomainGridlinesVisible(true); // 设置是否显示垂直方向背景,默认值为false
//		categoryplot.setDomainGridlinePaint(Color.red);//网格竖线颜色
//		categoryplot.setRangeGridlinePaint(Color.orange);//网格横线颜色
		categoryplot.setBackgroundPaint(Color.lightGray); // 背景色
		categoryplot.setNoDataMessage("No download history, please start the task");// 空数据提示
		categoryplot.setNoDataMessageFont(new Font("微软雅黑", 1, 25));// 字体
		categoryplot.setNoDataMessagePaint(Color.RED);// 字体颜色

		NumberAxis numberaxis = (NumberAxis) categoryplot.getRangeAxis();
		// numberaxis.setTickUnit(new NumberTickUnit(1));//指定Y轴数据间距
		numberaxis.setPositiveArrowVisible(true);// 正向箭头
		numberaxis.setTickLabelFont(new Font("微软雅黑", 1, 13));
		numberaxis.setUpperMargin(0.1);// 设置顶部数据与顶端的距离

		CategoryAxis domainAxis = (CategoryAxis) categoryplot.getDomainAxis();
		// 设置X轴标题与坐标字体
		domainAxis.setTickLabelFont(new Font("微软雅黑", 1, 12));
		domainAxis.setTickMarksVisible(true);// 用于显示X轴刻度
		// 设置X斜45
		// domainAxis.setCategoryLabelPositions(CategoryLabelPositions.UP_45);

		// 获取折线对象
		LineAndShapeRenderer renderer = (LineAndShapeRenderer) categoryplot.getRenderer();
		renderer.setBaseShapesVisible(true); // 数据点可视
		renderer.setBaseItemLabelGenerator(new StandardCategoryItemLabelGenerator()); // 显示数据点的数据
		renderer.setBaseItemLabelsVisible(true); // 显示折线图点上的数据

		BasicStroke realLine = new BasicStroke(1.8f); // 设置实线
		// 设置虚线
		float dashes[] = { 5.0f };
		BasicStroke brokenLine = new BasicStroke(2.2f, // 线条粗细
				BasicStroke.CAP_ROUND, // 端点风格
				BasicStroke.JOIN_ROUND, // 折点风格
				8f, dashes, 0.6f);

		return jfreechart;
	}
	//得到饼状图
	public static JFreeChart getPieChart() {
		JFreeChart chart = ChartFactory.createPieChart("Total Data Weight ", null, true, true, false);

		chart.getTitle().setFont(new Font("微软雅黑", Font.BOLD, 18));// 标题字体
		chart.getLegend().setItemFont(new Font("微软雅黑", Font.BOLD, 15));// 图例字体
		// 获取图表区域对象
		PiePlot categoryPlot = (PiePlot) chart.getPlot();
		categoryPlot.setLabelFont(new Font("微软雅黑", Font.BOLD, 15));// 标签字体
		categoryPlot.setBackgroundPaint(Color.lightGray); // 背景
		// 空数据提示
		categoryPlot.setNoDataMessage("No download history, please start the task");
		categoryPlot.setNoDataMessageFont(new Font("微软雅黑", 1, 25));// 字体的大�?
		categoryPlot.setNoDataMessagePaint(Color.RED);// 字体颜色

		// 设置图形的数据格式为(电商--总数(百分比))
		categoryPlot.setLabelGenerator(new StandardPieSectionLabelGenerator("{1}({2})"));
		
		return chart;
	}
	
	// 得到折线图数据
	public static DefaultCategoryDataset getLineDataSet(String url,String keyWord) {
		DefaultCategoryDataset defaultcategorydataset = new DefaultCategoryDataset();
		String[][] dataSet = Data.getScheduleData(url,keyWord);
		for (int i = 0; i < dataSet.length; i++) {
			defaultcategorydataset.addValue(Integer.valueOf(dataSet[i][0]), dataSet[i][1], dataSet[i][2]);
		}
		return defaultcategorydataset;
	}
	// 得到饼状图数据
	public static DefaultPieDataset getPieDataSet() {
		DefaultPieDataset defaultPieDataset = new DefaultPieDataset();
		String[][] dataSet = Data.downloadData();
		for (int i=0; i < dataSet.length; i++) {
			defaultPieDataset.setValue(dataSet[i][0],Integer.valueOf(dataSet[i][1]));
		}
		return defaultPieDataset;
	}

	// 保存为图片
	public static boolean savePicture(JFreeChart jfreechart) {
		File file = new File("./data/scnedule" + new SimpleDateFormat("yyyyMMddHHmmss").format(new Date()) + ".jpg");
		if (!file.exists()) {// 文件不存在则创建
			try {
				file.getParentFile().mkdirs();
				file.createNewFile();
				ChartUtilities.saveChartAsJPEG(file, 1.0f, jfreechart, 1200, 600);
			} catch (IOException e) {
				e.printStackTrace();
				return false;
			}
		}
		return true;
	}
}
