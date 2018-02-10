package team.qep.crawler.ui;

import java.awt.Color;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.util.HashMap;
import javax.swing.ButtonGroup;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import team.qep.crawler.util.Constant;

public class Setting extends JPanel implements MouseListener {
	private JFrame JF;
	private JLabel setting = new JLabel("设   置   中   心");
	
	private JLabel refresh = new JLabel("Refresh Interval :");
	private JComboBox<String> refreshInterval = new JComboBox<String>();//自动刷新间隔
	private JButton apply = new JButton();// 应用设置
	private JLabel theme = new JLabel("Theme :");
	private JRadioButton bw = new JRadioButton("黑&白");
	private JRadioButton color = new JRadioButton("炫 彩");
	private ButtonGroup group = new ButtonGroup();

	public Setting(JFrame ctlJF) {
		this.JF=ctlJF;
		this.Init();
		this.loadingData();
		this.setBounds();
		this.setColour();
		this.listener();
		
		group.add(bw);
		group.add(color);
		this.add(bw);
		this.add(color);
		this.add(theme);
		this.add(setting);
		this.add(refresh);
		this.add(refreshInterval);
		this.add(apply);
	}

	private void loadingData() {// 装载数据
		HashMap<String, String> map = Constant.Refresh;
		for (String key : map.keySet()) {
			refreshInterval.addItem(map.get(key));
		}
		
		if(Constant.Theme.equals("BlackWhite")){
			bw.setSelected(true);
		}else if(Constant.Theme.equals("Color")){
			color.setSelected(true);
		}
		refreshInterval.setSelectedItem(Constant.Refresh.get(Constant.RefreshInterval));
	}

	private void Init() {
		Init.initJLable(setting, "setting");
		Init.initJLable(refresh, "refresh");
		Init.initJLable(theme, "theme");
		Init.initJComboBox(refreshInterval, "refreshInterval");
		Init.initJRadioButton(bw, "bw");
		Init.initJRadioButton(color, "color");
		Init.initJButton(apply, "apply");
	}

	private void setBounds() {
		setting.setBounds(320, 0, 300, 35);
		refresh.setBounds(30, 70, 230, 35);
		refreshInterval.setBounds(260, 70, 200, 35);
		
		theme.setBounds(120, 160, 150, 35);
		bw.setBounds(260, 160, 100, 35);
		color.setBounds(360, 160, 100, 35);
		apply.setBounds(750, 520, 150, 40);
	}

	private void setColour() {
		this.setBackground(Theme.Panel9);
		setting.setFont(Theme.TitleFont);
		setting.setForeground(Theme.TitleColor);
		refresh.setFont(Theme.TitleFont);
		refresh.setForeground(Theme.TitleColor);
		theme.setFont(Theme.TitleFont);
		theme.setForeground(Theme.TitleColor);
		bw.setBackground(Theme.ButtonColor);
		color.setBackground(Theme.ButtonColor);
		apply.setBackground(Theme.ButtonColor);
		apply.setIcon(Constant.getIcon(apply,"apply"));
	}
	private void listener() {
		apply.addMouseListener(this);
	}

	public void mouseClicked(MouseEvent e) {// 单击
		if ("apply".equals(e.getComponent().getName())) {
			String theme=null;
			String refresh=null;

			if(bw.isSelected()){
				theme="BlackWhite";
			}else if(color.isSelected()){
				theme="Color";
			}
			HashMap<String, String> map = Constant.Refresh;
			for (String key : map.keySet()) {
				if(map.get(key).equals(refreshInterval.getSelectedItem().toString())){
					refresh=key;
					break;
				}
			}
			if(Constant.importSettings(theme,refresh)){
				Constant.exportSettings();// 导入设置
				Theme.setTheme(Constant.Theme);// 应用主题
				new UI();
				JF.dispose();
				new Promptinformation(null, "              更新成功", Constant.KeyValue.get("Info"));
			}else{
				new Promptinformation(null, "      更新失败,请检查配置文件", Constant.KeyValue.get("Info"));
			}
		} 
	}

	public void mousePressed(MouseEvent e) {// 按下
	}

	public void mouseReleased(MouseEvent e) {// 释放
	}

	public void mouseEntered(MouseEvent e) {// 进入
		if ("apply".equals(e.getComponent().getName())) {
			apply.setBackground(Color.WHITE);
		}
	}

	public void mouseExited(MouseEvent e) {// 离开
		if ("apply".equals(e.getComponent().getName())) {
			apply.setBackground(Theme.ButtonColor);
		}
	}
}
